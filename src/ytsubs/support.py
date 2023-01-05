from datetime import datetime, timezone
import sys

import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit

log = ccalogging.log
log.debug(f"importing {__name__} for {__appname__} v{__version__}")


def checkKeys(xdict, keys):
    try:
        if type(keys) is str:
            keys = [keys]
        for key in keys:
            if key not in xdict:
                return False
        return True
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkSubsKind(sub, kind="youtube#channel"):
    try:
        check = sub
        rabbithole = ["snippet", "resourceId", "kind"]
        for rh in rabbithole:
            if not checkKeys(check, rh):
                log.warning(f"missing key: {check=}, {rh=}, {sub=}, {rabbithole=}")
                return False
            check = check[rh]
        if check == kind:
            return True
        log.warning(f"not a youtube channel kind: {sub=}")
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkPLKind(item, kind="youtube#playlistItem"):
    try:
        if not checkKeys(item, "kind"):
            log.warning(f"playlist: missing key 'kind': {item=}")
            return False
        if kind == item["kind"]:
            return True
        log.warning(f"playlist: not a playlist kind: {item=}")
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkPLKindComplete(item):
    try:
        if not checkPLKind(item):
            return False
        check = item
        rabbithole = ["snippet", "resourceId", "videoId"]
        for rh in rabbithole:
            if not checkKeys(check, rh):
                log.warning(f"missing key: {check=}, {rh=}, {item=}, {rabbithole=}")
                return False
            check = check[rh]
        return True
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def checkVideoKind(resource, kind="youtube#video"):
    try:
        if not checkKeys(resource, "kind"):
            log.warning(f"video: missing key 'kind': {resource=}")
            return False
        if kind == resource["kind"]:
            return True
        log.warning(f"video: not a video kind: {resource=}")
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
        if not checkPLKindComplete(item):
            raise Exception(f"not a playlist item {item}")
        xl = ["title", "description", "channelTitle"]
        xd = {}
        for x in xl:
            xd[x] = item["snippet"][x]
        xd["timestamp"] = mkTimestamp(item["snippet"]["publishedAt"])
        xd["videoId"] = item["snippet"]["resourceId"]["videoId"]
        return xd
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
