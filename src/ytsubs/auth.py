import os
from pathlib import Path
import sys

import ccalogging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from ytsubs import __appname__, __version__

log = ccalogging.log
log.debug(f"importing {__name__} for {__appname__} v{__version__}")


def confDirectory():
    try:
        home = Path.home()
        confd = ".config"
        xconfd = os.environ.get("XDG_CONFIG_HOME", str(home.joinpath(confd)))
        confd = Path(xconfd)
        appconf = confd.joinpath(__appname__)
        if not appconf.exists():
            log.warning(f"Creating configuration directory: {appconf}")
            os.makedirs(appconf, exist_ok=True)
        return appconf
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def credsFiles():
    """returns a tuple of the fqfn for the client and session files."""
    try:
        confd = confDirectory()
        clientfn = confd.joinpath(f"{__appname__}-client.json")
        sessionfn = confd.joinpath(f"{__appname__}-session.json")
        log.debug(f"client file: {clientfn}")
        log.debug(f"session file: {sessionfn}")
        return (clientfn, sessionfn)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def authService():
    try:
        ytrwscope = "https://www.googleapis.com/auth/youtube"
        clientfn, sessionfn = credsFiles()
        store = Storage(sessionfn)
        creds = store.get()
        if creds is None or creds.invalid:
            log.debug(
                "session credentials not found or invalid, generating a new session"
            )
            msg = "OAuth 2.0 not configured, client secrets not found at {clientfn}"
            flow = flow_from_clientsecrets(clientfn, scope=ytrwscope, message=msg)
            creds = run_flow(flow, store, [])
        return creds
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
