import os
from pathlib import Path
import queue
import sys
import time

import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit
from ytsubs.api import (
    channelDetails,
    getAuthService,
    getSubscriptions,
    playlistVids,
    uploadPlaylistForChannel,
)
from ytsubs.download import makeVideo
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
        items = playlistVids(ytauth, plid, "")
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
        ytauth = getAuthService()
        chans = getSubs(ytauth)
        yesterday = int(time.time()) - 86400
        Q = queue.Queue()
        for chan in chans:
            items = getChanVids(ytauth, chan)
            items = [] if items is None else items
            for item in items:
                vd = vidDict(item)
                if vd["timestamp"] > yesterday:
                    log.debug(
                        f"adding '{vd['title']}' from channel '{vd['channelTitle']}' to Q"
                    )
                    Q.put(vd)
        log.info(f"There are {Q.qsize()} videos to download")
        while Q.qsize() > 0:
            item = Q.get()
            opfn, nfofn = makeVideo(item["videoId"], item["channelTitle"])
            log.info(f"{opfn=}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    ccalogging.setConsoleOut()
    ccalogging.setDebug()
    getVids()
