import os
from pathlib import Path
import queue
import sys
import time

import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit
from ytsubs.api import (
    getAuthService,
    getSubscriptions,
    playlistVids,
    uploadPlaylistForChannel,
)
from ytsubs.download import makeVideo
from ytsubs.nfo import makeFilmNfo
from ytsubs.support import vidDict

ccalogging.setLogFile("/home/chris/log/youtube.log")
ccalogging.setInfo()
log = ccalogging.log


def getSubs(ytauth):
    """Returns a list of channels you are subscribed to.

    each channel is a dict with these keys:
        publishedAt
        title
        description
        resourceId
        channelId
        thumbnails
    """
    try:
        chans = getSubscriptions(ytauth)
        return chans
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getChanVids(ytauth, chan):
    """Returns a list of the most recent video objects for a channel."""
    try:
        chanid = chan["resourceId"]["channelId"]
        chantitle = chan["title"]
        plid = uploadPlaylistForChannel(ytauth, chanid)
        items = playlistVids(ytauth, plid)
        return items
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def makeChannelDir(tvdir, channeld):
    try:
        opdir = tvdir.joinpath(channeld)
        os.makedirs(opdir, exist_ok=True)
        log.debug(f"created directory '{opdir}'")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getVids():
    try:
        days = 1
        if len(sys.argv) > 1:
            try:
                days = int(sys.argv[1])
            except ValueError:
                pass
        ytauth = getAuthService()
        chans = getSubs(ytauth)
        yesterday = int(time.time()) - (86400 * days)
        Q = queue.Queue()
        for chan in chans:
            items = getChanVids(ytauth, chan)
            items = [] if items is None else items
            for item in items:
                vd = vidDict(item)
                vd["publishedAt"] = item["snippet"]["publishedAt"]
                if vd["timestamp"] > yesterday:
                    log.debug(
                        f"adding '{vd['title']}' from channel '{vd['channelTitle']}' to Q"
                    )
                    Q.put(vd)
        log.info(f"There are {Q.qsize()} videos to download")
        while Q.qsize() > 0:
            item = Q.get()
            opfn, nfofn = makeVideo(item["videoId"], item["channelTitle"])
            log.info(f"{opfn=}\n{nfofn=}")
            fnfo = makeFilmNfo(item)
            with open(nfofn, "w") as nfofn:
                nfofn.write(fnfo)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getPlaylist(plid):
    try:
        ytauth = getAuthService()
        items = playlistVids(ytauth, plid)
        items = [] if items is None else items
        vitems = []
        for item in items:
            vd = vidDict(item)
            vd["publishedAt"] = item["snippet"]["publishedAt"]
            log.debug(
                f"adding '{vd['title']}' from channel '{vd['channelTitle']}' to Q"
            )
            vitems.append(vd)
        log.info(f"There are {len(vitems)} videos to download for playlist {plid}")
        plpath = f"/home/chris/youtube/playlist-{plid}"
        for item in vitems:
            opfn, nfofn = makeVideo(
                item["videoId"], item["channelTitle"], oppath=plpath
            )
            log.info(f"{opfn=}\n{nfofn=}")
            fnfo = makeFilmNfo(item)
            with open(nfofn, "w") as nfofn:
                nfofn.write(fnfo)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def setPlaylist():
    try:
        if len(sys.argv) != 2:
            print(f"usage: getplaylist <playlistid>")
            sys.exit(1)
        getPlaylist(sys.argv[1])
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    ccalogging.setConsoleOut()
    ccalogging.setDebug()
    # setPlaylist()
    getVids()
