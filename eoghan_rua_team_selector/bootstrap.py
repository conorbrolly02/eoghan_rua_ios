# eoghan_rua_team_selector/bootstrap.py
import os
import sys
import faulthandler
faulthandler.enable()

# Avoid .pyc writes into the read-only iOS bundle
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import traceback
from rubicon.objc import NSLog

def _excepthook(exc_type, exc, tb):
    msg = "".join(traceback.format_exception(exc_type, exc, tb))
    NSLog(f"BOOTSTRAP UNCAUGHT EXCEPTION:\n{msg}")

# Make *any* uncaught exception print to iOS syslog
sys.excepthook = _excepthook

# Import the real app; if it raises, log the full traceback.
try:
    from eoghan_rua_team_selector import app as real_app
    NSLog("BOOTSTRAP: real app imported OK")
except Exception as e:
    NSLog("BOOTSTRAP: import FAILED")
    _excepthook(type(e), e, e.__traceback__)
    raise

def main():
    try:
        return real_app.main()
    except Exception as e:
        _excepthook(type(e), e, e.__traceback__)
        raise
