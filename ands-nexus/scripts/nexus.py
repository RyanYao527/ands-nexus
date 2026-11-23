#!/usr/bin/env python3
"""Entry point for the optional ANDS local Agent."""
import argparse
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

if sys.version_info < (3, 11):
    print('ANDS Agent requires Python 3.11 or newer', file=sys.stderr)
    raise SystemExit(2)

from nexus_runtime.engine import Engine
from nexus_runtime.store import NexusError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, help='Explicit local project directory')
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('--goal', required=True)
    init.add_argument('--repo')
    init.add_argument('--member', action='append', default=[], metavar='ROLE=LOGIN')
    init.add_argument('--input', action='append', default=[], type=Path)
    for name in ('status', 'plan', 'step', 'run', 'sync', 'pause', 'stop'):
        command = commands.add_parser(name)
        command.add_argument('workflow_id')
    approve = commands.add_parser('approve', help='Human-only: approve exactly the displayed plan')
    approve.add_argument('workflow_id')
    approve.add_argument('--version', required=True, type=int)
    approve.add_argument('--hash', required=True)
    accept = commands.add_parser('accept', help='Human-only: accept a reviewed file by hash')
    accept.add_argument('workflow_id')
    accept.add_argument('--task', required=True)
    accept.add_argument('--hash', required=True)
    revise = commands.add_parser('revise', help='Human-only: request a revision')
    revise.add_argument('workflow_id')
    revise.add_argument('--task', required=True)
    revise.add_argument('--reason', required=True)
    submit = commands.add_parser('submit')
    submit.add_argument('workflow_id')
    submit.add_argument('--task', required=True)
    submit.add_argument('--path', required=True, type=Path)
    resume = commands.add_parser('resume')
    resume.add_argument('workflow_id')
    resume.add_argument('--extra-invocations', default=0, type=int)
    resume.add_argument('--extra-seconds', default=0, type=int)
    doctor = commands.add_parser('doctor')
    doctor.add_argument('--live', action='store_true', help='Run two real restricted-worker probes; uses the existing Codex login')
    args = parser.parse_args()
    try:
        human_command = args.command in ('approve', 'accept', 'revise') or (args.command == 'resume' and (args.extra_invocations or args.extra_seconds))
        if human_command and not (sys.stdin.isatty() and sys.stdout.isatty()):
            raise NexusError('human decision must be entered directly in an interactive terminal; agents must not pipe or replay it')
        engine = Engine(args.workspace)
        if args.command == 'init':
            members = {}
            for item in args.member:
                if '=' not in item:
                    raise NexusError('member must have ROLE=LOGIN form')
                role, login = item.split('=', 1)
                if role in members:
                    raise NexusError('duplicate member role')
                members[role] = login
            value = engine.init(args.goal, repo=args.repo, members=members, inputs=args.input)
        elif args.command == 'doctor':
            skill_root = Path(__file__).resolve().parent.parent
            value = {'skill_version': (skill_root / 'VERSION').read_text(encoding='utf-8-sig').strip(),
                     'skill_root': str(skill_root), 'python': sys.version.split()[0],
                     'codex': shutil.which('codex'), 'gh': shutil.which('gh'), 'live_probe_run': False}
            if args.live:
                from nexus_runtime.worker import CodexWorker
                value['probe'] = CodexWorker(evidence_dir=engine.store.control / 'runs').probe()
                value['live_probe_run'] = True
                if value['probe'].get('passed') is not True:
                    raise NexusError('restricted worker isolation probe did not pass')
        elif args.command == 'approve':
            value = engine.approve(args.workflow_id, args.version, args.hash)
        elif args.command == 'accept':
            value = engine.accept(args.workflow_id, args.task, args.hash)
        elif args.command == 'revise':
            value = engine.revise(args.workflow_id, args.task, args.reason)
        elif args.command == 'submit':
            value = engine.submit(args.workflow_id, args.task, args.path)
        elif args.command == 'resume':
            value = engine.resume(args.workflow_id, args.extra_invocations, args.extra_seconds)
        elif args.command == 'step':
            value = engine.run(args.workflow_id, once=True)
        else:
            value = getattr(engine, args.command)(args.workflow_id)
        if 'inputs' in value:
            value['inputs'] = [{k: v for k, v in source.items() if k != 'content'} for source in value['inputs']]
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return 3 if value.get('status') == 'paused' and value.get('last_error') else 0
    except (NexusError, OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
