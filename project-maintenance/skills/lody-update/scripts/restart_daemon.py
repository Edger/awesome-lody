#!/usr/bin/env python3
"""Restart an installed macOS standalone daemon; persist verified completion."""
import argparse
import json
import os
from pathlib import Path
import plistlib
import re
import subprocess
import sys
import time

ANSI = re.compile(r'\x1b\[[0-9;]*m')


def connected(status, machine):
    """Fail closed when the current CLI status format lacks required evidence."""
    status = ANSI.sub('', status)
    fields = dict(re.findall(r'^\s*(Phase|Stage|Connectivity|Backend Auth|Backend Link|Machine ID|Workspaces):\s*(.*?)\s*$', status, re.M))
    backends = re.findall(r'^\s*Backend:\s*(\S+)', status, re.M)
    return ('Daemon is running' in status
            and all(fields.get(k) == v for k, v in {
                'Phase': 'running', 'Stage': 'ready', 'Connectivity': 'online',
                'Backend Auth': 'authorized', 'Backend Link': 'connected',
                'Machine ID': machine}.items())
            and fields.get('Workspaces', '').isdigit()
            and int(fields['Workspaces']) > 0
            and len(backends) == int(fields['Workspaces'])
            and all(x == 'connected' for x in backends))


def clean_env():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(('LODY_SUPERVISOR_', 'LODY_ELECTRON_')) or key in {
            'ELECTRON_RUN_AS_NODE', 'LODY_SESSION_ID', 'LODY_WORKSPACE_SESSION_ID',
            'LODY_MCP_SESSION_ID', 'LODY_DAEMON_SUPERVISED'}:
            env.pop(key, None)
    return env


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--launcher', required=True, type=Path)
    p.add_argument('--version', required=True)
    p.add_argument('--machine-id', required=True)
    p.add_argument('--app', type=Path, default=Path('/Applications/Lody.app'))
    p.add_argument('--data-dir', type=Path, default=Path.home() / '.lody')
    p.add_argument('--task-dir', required=True, type=Path)
    p.add_argument('--ready-timeout', type=int, default=120)
    p.add_argument('--check-only', action='store_true')
    p.add_argument('--detach', action='store_true')
    args = p.parse_args()
    if not args.task_dir.is_absolute():
        p.error('Use an absolute task directory')
    if sys.platform != 'darwin':
        p.error('This helper supports macOS only')
    if not args.launcher.is_absolute() or not args.launcher.is_file():
        p.error('Use an existing absolute stable launcher path')
    env = clean_env()
    if args.detach:
        args.task_dir.mkdir(parents=True, exist_ok=False)
        with (args.task_dir / 'task.log').open('ab') as log:
            command = [sys.executable, str(Path(__file__).resolve())] + [x for x in sys.argv[1:] if x != '--detach']
            child = subprocess.Popen(command, env=env, stdin=subprocess.DEVNULL,
                                     stdout=log, stderr=log, start_new_session=True)
        (args.task_dir / 'task.pid').write_text(str(child.pid))
        print(json.dumps({'submitted': True, 'pid': child.pid, 'taskDir': str(args.task_dir)}))
        return 0
    args.task_dir.mkdir(parents=True, exist_ok=True)
    result_path = args.task_dir / 'result.json'
    if result_path.exists():
        p.error('Use a fresh task directory; existing results are never overwritten')
    stage = 'preflight'
    reopen = False
    workspace_ids = set()

    def run(command, timeout=90):
        r = subprocess.run([str(x) for x in command], env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        print(r.stdout, flush=True)
        if r.returncode:
            raise RuntimeError('Command failed: ' + str(command[0]) + ' exit ' + str(r.returncode))
        return r.stdout

    def processes():
        out = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,command='], text=True)
        return {int(a): (int(b), c) for line in out.splitlines()
                for a, b, c in [line.strip().split(None, 2)]}

    app_info = {}
    executable = None

    def app_running():
        return any(cmd == executable for _, cmd in processes().values())

    def verify():
        status = run([args.launcher, 'daemon', 'status'], 15)
        record = json.loads((args.data_dir / 'run/daemon.json').read_text())
        procs = processes()
        parent, command = procs.get(record['pid'], (None, ''))
        owner = procs.get(parent, (None, ''))[1]
        if (record.get('version') == args.version and connected(status, args.machine_id)
                and set(re.findall(r'^\s+ID:\s*(\S+)', ANSI.sub('', status), re.M)) == workspace_ids
                and 'lody' in command and re.search(r'\bstart(?:\s|$)', command)
                and re.search(r'\bdaemon-runner(?:\s|$)', owner)):
            return record
        raise RuntimeError('Runtime version, ownership or connectivity is not ready')

    def await_ready():
        deadline = time.monotonic() + args.ready_timeout
        while True:
            try:
                return verify()
            except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
                if time.monotonic() >= deadline:
                    raise RuntimeError('Readiness deadline exceeded: ' + str(error)) from error
                time.sleep(2)

    try:
        if args.app.exists():
            with (args.app / 'Contents/Info.plist').open('rb') as f:
                app_info = plistlib.load(f)
            executable = str(args.app / 'Contents/MacOS' / app_info['CFBundleExecutable'])
        installed = ANSI.sub('', run([args.launcher, '--version'])).splitlines()
        if args.version not in installed:
            raise RuntimeError('Installed CLI does not match target version')
        initial = run([args.launcher, 'daemon', 'status'])
        workspace_ids = set(re.findall(r'^\s+ID:\s*(\S+)', ANSI.sub('', initial), re.M))
        if not workspace_ids or not connected(initial, args.machine_id):
            raise RuntimeError('Initial machine/connection must be verified before restarting')
        if not args.check_only:
            if 'Local agent Host: electron' in initial or 'Daemon is running' not in initial:
                raise RuntimeError('This helper only restarts an existing standalone daemon')
            reopen = app_running()
            if reopen:
                stage = 'quit-desktop'
                run(['osascript', '-e', 'tell application id ' + json.dumps(app_info['CFBundleIdentifier']) + ' to quit'], 30)
                deadline = time.monotonic() + 45
                while app_running() and time.monotonic() < deadline:
                    time.sleep(1)
                if app_running():
                    raise RuntimeError('Desktop did not exit; no forced termination attempted')
            stage = 'stop-daemon'
            run([args.launcher, 'daemon', 'stop'])
            stage = 'start-daemon'
            run([args.launcher, 'daemon', 'start'])
        stage = 'verify-daemon'
        record = await_ready()
        if reopen:
            stage = 'reopen-desktop'
            run(['open', '-a', args.app], 30)
            deadline = time.monotonic() + 30
            while not app_running() and time.monotonic() < deadline:
                time.sleep(1)
            if not app_running():
                raise RuntimeError('Desktop did not reopen')
            time.sleep(5)
            stage = 'verify-after-reopen'
            record = await_ready()
        result = {'ok': True, 'stage': 'complete', 'machineId': args.machine_id, 'runtime': record}
    except Exception as error:
        result = {'ok': False, 'stage': stage, 'error': str(error)}
        if reopen:
            try:
                run(['open', '-a', args.app], 30)
                result['desktopRecovery'] = 'open requested; service health unverified'
            except Exception as recovery_error:
                result['desktopRecovery'] = str(recovery_error)
    temp = result_path.with_suffix('.tmp')
    temp.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    temp.replace(result_path)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
