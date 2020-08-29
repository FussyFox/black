#!/usr/bin/env python
"""Lambda function that executes Black, a static file linter."""
from lintipy import CheckRun

handle = CheckRun.as_handler("black", "black", "--check", "--diff", ".")
