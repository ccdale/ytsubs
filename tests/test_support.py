from ytsubs.support import (
    checkKeys,
    checkPLKind,
    checkVideoKind,
    mkTimestamp,
    vidDict,
)


def test_mkTimestamp():
    timestr = "2023-01-01T15:00:18Z"
    ts = mkTimestamp(timestr)
    assert 1672585218 == ts


def test_checkVideoKind():
    x = {"kind": "youtube#video", "videoId": "UlOKNKLd99w"}
    assert checkVideoKind(x)


def test_checkPLKind():
    x = {"kind": "youtube#playlistItem"}
    assert checkPLKind(x)


def test_checkKeys():
    x = {"one": 1, "two": 2, "three": 3}
    y = ["one", "two", "three"]
    assert checkKeys(x, y)


def test_checkKeys_missing_key():
    x = {"one": 1, "two": 2, "three": 3}
    y = ["one", "two", "three", "four"]
    assert False == checkKeys(x, y)
