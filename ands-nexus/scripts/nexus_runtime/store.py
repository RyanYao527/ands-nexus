"""Transactional checkpoints and a single-writer lock per workflow."""
from contextlib import contextmanager
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import uuid


class NexusError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def contained(root, path):
    root, path = Path(root).resolve(), Path(path)
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise NexusError('path is outside the approved workspace or is a symbolic link')
    return path.resolve()


def process_alive(pid):
    if os.name == 'nt':
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, int(pid))
        if not handle:
            # Access denied is not proof of a dead owner.
            return ctypes.get_last_error() == 5
        try:
            code = ctypes.c_ulong()
            if not kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(code)):
                return True
            return code.value == 259
        finally:
            kernel.CloseHandle(ctypes.c_void_p(handle))
    try:
        stat = Path('/proc', str(pid), 'stat')
        if stat.exists() and stat.read_text().rsplit(')', 1)[1].strip().startswith('Z'):
            return False
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def process_identity(pid):
    """Prevent a stale/reused PID from authorizing termination of another process."""
    if not process_alive(pid):
        return None
    if os.name == 'nt':
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, int(pid))
        if not handle:
            return None
        try:
            created, exited, system, user = (ctypes.c_ulonglong() for _ in range(4))
            size = ctypes.c_ulong(32768)
            image = ctypes.create_unicode_buffer(size.value)
            if not kernel.GetProcessTimes(ctypes.c_void_p(handle), ctypes.byref(created), ctypes.byref(exited), ctypes.byref(system), ctypes.byref(user)):
                return None
            if not kernel.QueryFullProcessImageNameW(ctypes.c_void_p(handle), 0, image, ctypes.byref(size)):
                return None
            return dict(pid=pid, created=created.value, image=image.value)
        finally:
            kernel.CloseHandle(ctypes.c_void_p(handle))
    try:
        stat = Path('/proc', str(pid), 'stat').read_text()
        return dict(pid=pid, created=stat[stat.rfind(')') + 2:].split()[19], image=os.readlink('/proc/' + str(pid) + '/exe'))
    except (OSError, IndexError):
        return None


class Store:
    def __init__(self, workspace):
        self.root = Path(workspace).resolve()
        if not self.root.is_dir():
            raise NexusError('workspace must be an existing directory')
        self.control = contained(self.root, self.root / '.nexus')
        self.control.mkdir(exist_ok=True)
        self.path = contained(self.root, self.control / 'state.sqlite3')
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS workflows(id TEXT PRIMARY KEY, data TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY, workflow_id TEXT, at TEXT, kind TEXT, data TEXT);
                CREATE TABLE IF NOT EXISTS locks(workflow_id TEXT PRIMARY KEY, pid INTEGER, token TEXT);
                CREATE TABLE IF NOT EXISTS hosted_failures(
                    workflow_id TEXT, request_id TEXT, request_hash TEXT, response_sha256 TEXT, receipt TEXT NOT NULL,
                    PRIMARY KEY(workflow_id,request_id,request_hash,response_sha256));
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.execute('PRAGMA synchronous=FULL')
        try:
            with db:
                yield db
        finally:
            db.close()

    def create(self, state):
        with self.connect() as db:
            db.execute('INSERT INTO workflows VALUES (?, ?)', (state['id'], json.dumps(state, ensure_ascii=False)))
            db.execute('INSERT INTO events(workflow_id,at,kind,data) VALUES (?,?,?,?)', (state['id'], now(), 'created', '{}'))

    def load(self, workflow_id):
        with self.connect() as db:
            row = db.execute('SELECT data FROM workflows WHERE id=?', (workflow_id,)).fetchone()
        if row is None:
            raise NexusError('unknown workflow: ' + workflow_id)
        return json.loads(row[0])

    def hosted_failure(self, workflow_id, request_id, request_hash, response_sha256):
        with self.connect() as db:
            row = db.execute('SELECT receipt FROM hosted_failures WHERE workflow_id=? AND request_id=? AND request_hash=? AND response_sha256=?',
                             (workflow_id, request_id, request_hash, response_sha256)).fetchone()
        return json.loads(row[0]) if row else None

    def remember_hosted_failure(self, workflow_id, request_id, request_hash, response_sha256, receipt):
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO hosted_failures VALUES (?,?,?,?,?)',
                       (workflow_id, request_id, request_hash, response_sha256, json.dumps(receipt, ensure_ascii=False)))
        return self.hosted_failure(workflow_id, request_id, request_hash, response_sha256)

    def change(self, workflow_id, kind, mutate):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT data FROM workflows WHERE id=?', (workflow_id,)).fetchone()
            if row is None:
                raise NexusError('unknown workflow: ' + workflow_id)
            state = json.loads(row[0])
            previous = json.loads(row[0])
            allowed_after_halt = {'stopped_by_user', 'paused_error', 'worker_elapsed', 'probe_elapsed',
                                  'operation_done', 'operation_error', 'operation_elapsed', 'remote_observed', 'worker_finished', 'run_elapsed', 'hosted_request_expired'}
            if state['status'] == 'stopped' and kind not in allowed_after_halt:
                raise NexusError('stopped workflow cannot advance')
            if state['status'] == 'paused' and kind not in allowed_after_halt | {'resumed', 'paused_by_user'}:
                raise NexusError('paused workflow needs explicit resume')
            old_status = state['status']
            result = mutate(state)
            if old_status == 'stopped' and state['status'] != 'stopped':
                raise NexusError('stopped workflow cannot be resumed by a result')
            state['updated_at'] = now()
            changes = {key: value for key, value in state.items() if key not in previous or value != previous[key]}
            removed = [key for key in previous if key not in state]
            db.execute('UPDATE workflows SET data=? WHERE id=?', (json.dumps(state, ensure_ascii=False), workflow_id))
            db.execute('INSERT INTO events(workflow_id,at,kind,data) VALUES (?,?,?,?)', (workflow_id, now(), kind, json.dumps(dict(changes=changes, removed=removed, result=result), ensure_ascii=False)))
        return state

    @contextmanager
    def lock(self, workflow_id):
        token = uuid.uuid4().hex
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT pid FROM locks WHERE workflow_id=?', (workflow_id,)).fetchone()
            if row and process_alive(row[0]):
                raise NexusError('workflow already has an active writer')
            workflow = db.execute('SELECT data FROM workflows WHERE id=?', (workflow_id,)).fetchone()
            if workflow:
                data = json.loads(workflow[0])
                child = data.get('worker_pid') if data.get('execution_mode', 'restricted-native') == 'restricted-native' else None
                if child and process_alive(child):
                    raise NexusError('orphan worker still active; stop that recorded process before recovery')
            db.execute('INSERT OR REPLACE INTO locks VALUES (?,?,?)', (workflow_id, os.getpid(), token))
        try:
            yield
        finally:
            with self.connect() as db:
                db.execute('DELETE FROM locks WHERE workflow_id=? AND token=?', (workflow_id, token))
