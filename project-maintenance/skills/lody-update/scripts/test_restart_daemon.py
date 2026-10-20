"""Regression checks; all process and service mutations are mocked."""
import contextlib
import io
import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import restart_daemon as helper

STATUS = '''Daemon is running
 Phase: running
 Stage: ready
 Connectivity: online
 Backend Auth: authorized
 Backend Link: connected
 Workspaces: 1
   ID: workspace
   Backend: connected
 Machine ID: machine
'''


class RestartTests(unittest.TestCase):
    def test_connection_requires_all_evidence(self):
        self.assertTrue(helper.connected(STATUS, 'machine'))
        for text in (STATUS.replace('authorized', 'pending'),
                     STATUS.replace('Backend: connected', 'Backend: disconnected'),
                     STATUS.replace('Workspaces: 1', 'Workspaces: 2'),
                     STATUS.replace('Stage: ready', ''),
                     STATUS.replace('Machine ID: machine', 'Machine ID: other')):
            self.assertFalse(helper.connected(text, 'machine'))

    def scenario(self, fail_quit=False, final_status=STATUS, version='target', initial=STATUS):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            launcher = root / 'lody'
            launcher.touch()
            app = root / 'Lody.app'
            (app / 'Contents').mkdir(parents=True)
            (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
                'CFBundleExecutable': 'Lody', 'CFBundleIdentifier': 'test.lody'}))
            (root / 'run').mkdir()
            (root / 'run/daemon.json').write_text(json.dumps({'pid': 2, 'version': version}))
            calls, state = [], {'app': True, 'statuses': 0}
            def run(command, **kwargs):
                calls.append(command)
                output, code = '', 0
                if command[-1] == '--version': output = 'target\n'
                elif command[-1] == 'status':
                    output = initial if state['statuses'] == 0 else final_status
                    state['statuses'] += 1
                elif command[0] == 'osascript':
                    code = 1 if fail_quit else 0
                    if not code: state['app'] = False
                elif command[0] == 'open': state['app'] = True
                return subprocess.CompletedProcess(command, code, output)
            def ps(*args, **kwargs):
                return ('1 0 node /prefix/bin/lody daemon-runner\n'
                        '2 1 node /prefix/bin/lody start\n' +
                        (f'3 0 {app}/Contents/MacOS/Lody\n' if state['app'] else ''))
            argv = ['restart', '--launcher', str(launcher), '--version', 'target',
                    '--machine-id', 'machine', '--app', str(app), '--data-dir', str(root),
                    '--task-dir', str(root / 'task'), '--ready-timeout', '0']
            with patch.object(sys, 'argv', argv), patch.object(helper.subprocess, 'run', run), \
                 patch.object(helper.subprocess, 'check_output', ps), \
                 patch.object(helper.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
                exit_code = helper.main()
            return exit_code, json.loads((root / 'task/result.json').read_text()), calls

    def test_quit_before_stop_and_reverify_after_open(self):
        code, result, calls = self.scenario()
        self.assertEqual(code, 0)
        self.assertTrue(result['ok'])
        names = [str(x[-1]) if x[0] not in ('open', 'osascript') else x[0] for x in calls]
        self.assertLess(names.index('osascript'), names.index('stop'))
        self.assertLess(names.index('stop'), names.index('start'))
        self.assertEqual(names[-2:], ['open', 'status'])

    def test_quit_failure_preserves_daemon(self):
        _, result, calls = self.scenario(fail_quit=True)
        self.assertFalse(result['ok'])
        self.assertFalse(any(x[-1] in ('stop', 'start') for x in calls))

    def test_runtime_and_connection_failures_never_succeed(self):
        for kwargs in ({'version': 'old'},
                       {'final_status': STATUS.replace('Backend: connected', 'Backend: disconnected')},
                       {'final_status': STATUS.replace('ID: workspace', 'ID: different')}):
            code, result, _ = self.scenario(**kwargs)
            self.assertEqual(code, 1)
            self.assertFalse(result['ok'])

    def test_wrong_machine_causes_no_mutation(self):
        _, result, calls = self.scenario(initial=STATUS.replace('Machine ID: machine', 'Machine ID: other'))
        self.assertFalse(result['ok'])
        self.assertTrue(all(x[-1] in ('status', '--version') for x in calls))


if __name__ == '__main__':
    unittest.main()
