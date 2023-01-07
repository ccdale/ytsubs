import httplib2
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit
from ytsubs.auth import authService
from ytsubs.support import checkSubsKind

log = ccalogging.log
log.debug(f"importing {__name__} for {__appname__} v{__version__}")


def getAuthService():
    try:
        ytapiname = "youtube"
        ytversion = "v3"
        creds = authService()
        http = creds.authorize(httplib2.Http())
        built = build(ytapiname, ytversion, http=http)
        return built
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getSubscriptions(auth):
    try:
        nextpage = ""
        cn = 0
        chans = []
        while True:
            log.debug(f"retrieving subs page {cn + 1}")
            subs = subscriptions(auth, nextpage)
            for s in subs.get("items", []):
                if checkSubsKind(s):
                    chans.append(s["snippet"])
            if "nextPageToken" not in subs:
                break
            nextpage = subs["nextPageToken"]
            cn += 1
        log.debug(f"retrieved {len(chans)} channels")
        return chans
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def subscriptions(ytauth, nextpage):
    try:
        kwargs = {
            "part": "snippet",
            "mine": True,
            "maxResults": 50,
            "order": "alphabetical",
            "pageToken": nextpage,
        }
        subs = ytauth.subscriptions().list(**kwargs).execute()
        return subs
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def channelDetails(ytauth, cid, nextpage):
    try:
        kwargs = {"id": cid, "part": "contentDetails", "pageToken": nextpage}
        chansdetails = ytauth.channels().list(**kwargs).execute()
        return chansdetails
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def playlistVids(ytauth, plid):
    try:
        items = []
        kwargs = {"playlistId": plid, "part": "snippet", "pageToken": nextpage}
        plvids = {"nextPageToken": "first"}
        while plvids["nextPageToken"] != "":
            plvids = ytauth.playlistItems().list(**kwargs).execute()
            items.extend(plvids["items"])
            kwargs["pageToken"] = plvids["nextPageToken"]
        return items
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def uploadPlaylistForChannel(ytauth, cid):
    try:
        cd = channelDetails(ytauth, cid, "")
        log.debug(f"channel details: {cd}")
        items = cd.get("items", None)
        if not items:
            raise Exception(f"items not in {cd}")
        item = items[0]
        dets = item.get("contentDetails", None)
        if not dets:
            raise Exception(f"dets not in {item}")
        rp = dets.get("relatedPlaylists", None)
        if not rp:
            raise Exception(f"rp not in {dets}")
        up = rp.get("uploads", None)
        if not up:
            raise Exception(f"up not in {rp}")
        return up
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
