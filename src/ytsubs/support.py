from datetime import datetime, timezone
import sys

import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit

log = ccalogging.log
log.debug(f"importing {__name__} for {__appname__} v{__version__}")


def checkSubsKind(sub, kind="youtube#channel"):
    try:
        thing = None if "snippet" not in sub else sub["snippet"]
        thing = (
            None if thing is None or "resourceId" not in thing else thing["resourceId"]
        )
        thing = None if thing is None or "kind" not in thing else thing["kind"]
        if thing and thing == kind:
            return True
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkPLKind(item, kind="youtube#playlistItem"):
    try:
        thing = None if "kind" not in item else item["kind"]
        if kind == thing:
            return True
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkVideoKind(resource, kind="youtube#video"):
    try:
        thing = None if "kind" not in resource else resource["kind"]
        if kind == thing:
            return True
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def mkTimestamp(timestr):
    """make a unix timestamp, assuming UTC.

    timestr: '2023-01-01T15:00:18Z'
    """
    try:
        tmstr = timestr[:-1] if timestr.endswith("Z") else timestr
        dt = datetime.fromisoformat(tmstr).astimezone(timezone.utc)
        return int(dt.timestamp())
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def vidDict(item):
    try:
        if not checkPLKind(item):
            raise Exception(f"not a playlist item {item}")
        if "snippet" not in item:
            raise Exception(f"bad video item {item}")
        if "resourceId" not in item["snippet"]:
            raise Exception(f"no video id in snippet {item['snippet']}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
