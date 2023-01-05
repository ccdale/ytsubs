import os
from pathlib import Path
import sys

import ccalogging

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit
from ytsubs.api import (
    channelDetails,
    getAuthService,
    getSubscriptions,
    playlistVids,
    uploadPlaylistForChannel,
)

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
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def makeChannelDir(tvdir, channeld):
    try:
        opdir = tvdir.joinpath(channeld)
        os.makedirs(opdir, exist_ok=True)
        log.debug(f"created directory '{opdir}'")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    ccalogging.setConsoleOut()
    ccalogging.setDebug()
    tvdir = Path("/home/chris/seagate4/youtube")
    ytauth = getAuthService()
    chans = getSubs(ytauth)
    for cn, chan in enumerate(chans):
        upl = uploadPlaylistForChannel(ytauth, chan["resourceId"]["channelId"])
        items = playlistVids(ytauth, upl, "")
        print(f'{chan["resourceId"]["channelId"]} {chan["title"]} items: {items}')
        if cn > 10:
            break
