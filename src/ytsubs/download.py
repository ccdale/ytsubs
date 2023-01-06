import os
import re
import sys
import unicodedata

import ccalogging
from pytube import YouTube

from ytsubs import __appname__, __version__, errorNotify, errorRaise, errorExit

log = ccalogging.log
log.debug(f"importing {__name__} for {__appname__} v{__version__}")


def makeVideo(vid, ytchan, oppath="/home/chris/youtube"):
    try:
        url = f"http://youtube.com/watch?v={vid}"
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        title = yt.title
        schan = slugify(ytchan)
        stitle = slugify(title)
        opdir = os.path.join(oppath, schan)
        os.makedirs(opdir, exist_ok=True)
        opfqfn = os.path.join(opdir, stitle)
        opfn = f"{stitle}.mp4"
        nfofn = f"{os.path.join(opdir, stitle)}.nfo"
        log.debug(f"{opfqfn=} {nfofn=}")
        yt.streams.get_highest_resolution().download(output_path=opdir, filename=opfn)
        return (opfn, nfofn)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


if __name__ == "__main__":
    # vid = "BWQhlulTAyY"
    # vid = "4zZuPfAYS2Y"
    # vid = "3ncFpP8GP4g"
    vid = "PnoyjPRAmRk"
    ytchan = "Channel 4 Entertainment"
    opfn, nfofn = makeVideo(vid, ytchan)
    print(f"{opfn=} {nfofn=}")
