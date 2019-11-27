"""Lambda function that executes Black, a static file linter."""
import logging
import os
import resource
import subprocess
import sys
import glob

from lintipy import CheckRun, COMPLETED, TIMED_OUT

root_logger = logging.getLogger('')
logger = logging.getLogger('black')
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(logging.StreamHandler(sys.stdout))


class BlackCheckRun(CheckRun):
    cmd_timeout = 1

    def run_process(self, code_path):
        code = 0
        cmd = ' '.join(('python', '-m', self.cmd) + self.cmd_args)
        log = "$ %s .\n" % cmd
        for file_name in glob.glob(os.path.join(code_path, 'tests/**.py'), recursive=True):
            if os.path.isfile(file_name):
                try:
                    logger.info('Running: %s', cmd)
                    process = subprocess.run(  # nosec
                        ('python', '-m', self.cmd) + self.cmd_args + (file_name,),
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        cwd=code_path, env=self.get_env(),
                        timeout=self.cmd_timeout,
                    )
                except subprocess.TimeoutExpired:
                    self.update_check_run(
                        COMPLETED, 'Command timed out after %ss' % self.cmd_timeout, TIMED_OUT
                    )
                    raise
                else:
                    info = resource.getrusage(resource.RUSAGE_CHILDREN)
                    lines = process.stdout.decode().splitlines()
                    log += '\n'.join(lines[:-2])
                    logger.debug(log)
                    logger.debug('exit %s', process.returncode)
                    logger.info(
                        'linter exited with status code %s in %ss' % (process.returncode, info.ru_utime)
                    )
                    code &= process.returncode
        return code, log


handle = BlackCheckRun.as_handler(
    'black',
    'black', '--check', '--diff', '.'
)
