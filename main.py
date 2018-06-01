"""Lambda function that executes Black, a static file linter."""
import logging
import sys

from lintipy import CheckRun

root_logger = logging.getLogger('')
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(logging.StreamHandler(sys.stdout))


def handle(*args, **kwargs):
    """Handle that is invoked by AWS lambda."""
    CheckRun(
        'black',
        'black', '--check', '.'
    )(*args, **kwargs)
