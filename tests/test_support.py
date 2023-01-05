from ytsubs.support import (
    checkKeys,
    checkPLKind,
    checkSubsKind,
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


def test_checkVideoKind_missing_kind():
    x = {"eric": "youtube#video", "videoId": "UlOKNKLd99w"}
    assert False == checkVideoKind(x)


def test_checkVideoKind_not_video():
    x = {"kind": "youtube#eric", "videoId": "UlOKNKLd99w"}
    assert False == checkVideoKind(x)


def test_checkPLKind():
    x = {"kind": "youtube#playlistItem"}
    assert checkPLKind(x)


def test_checkPLKind_missing_kind():
    x = {"eric": "youtube#playlistItem"}
    assert False == checkPLKind(x)


def test_checkPLKind_not_playlist():
    x = {"kind": "youtube#eric"}
    assert False == checkPLKind(x)


def test_checkSubsKind():
    x = {"snippet": {"resourceId": {"kind": "youtube#channel"}}}
    assert checkSubsKind(x)


def test_checkSubsKind_missing_kind():
    x = {"snippet": {"resourceId": {"eric": "youtube#channel"}}}
    assert False == checkSubsKind(x)


def test_checkSubsKind_not_channel():
    x = {"snippet": {"resourceId": {"kind": "eric#channel"}}}
    assert False == checkSubsKind(x)


def test_checkKeys():
    x = {"one": 1, "two": 2, "three": 3}
    y = ["one", "two", "three"]
    assert checkKeys(x, y)


def test_checkKeys_missing_key():
    x = {"one": 1, "two": 2, "three": 3}
    y = ["one", "two", "three", "four"]
    assert False == checkKeys(x, y)


def test_checkKeys_str_input():
    x = {"one": 1, "two": 2, "three": 3}
    y = "two"
    assert checkKeys(x, y)


def test_vidDict():
    item = {
        "kind": "youtube#playlistItem",
        "etag": "DZhMN19k2-9r-lMTopbXexvVlL0",
        "id": "VVV4bjcwVGNTd0ExOEI5Mk95OHl1QV9RLlVsT0tOS0xkOTl3",
        "snippet": {
            "publishedAt": "2023-01-01T15:00:18Z",
            "channelId": "UCxn70TcSwA18B92Oy8yuA_Q",
            "title": "Ten British 80s Sitcoms You DEFINITELY Don't Remember",
            "description": "So how many of these 80s British Sitcoms do you remember?\nEven More British 80s  Sitcoms  You Probably Don't Remember (80s uk sitcoms list)\n\nMarti Caine Tribute:  https://youtu.be/Rt9dD9KHvgc\n\nSitcoms,best 80s british sitcoms,top 10 british 80s sitcoms,british t.v. sitcoms in the 80s,british tv sitcoms of the 80s,80s british family sitcoms,uk 80s sitcoms,80's uk sitcoms list,80s uk sitcom theme songs,80s uk comedy sitcoms,late 80s uk sitcoms,top 10 80's uk sitcoms\nHello, and welcome to The Foot Of Our Stairs\n\n\nFacebook:  https://www.facebook.com/footothestairs\n\nTwitter:  https://twitter.com/footothestairs\n\n\n\n\n80s british sitcoms,comedy,british 80s sitcoms,classic 80s british sitcoms,best 80s british sitcoms,top 10 british 80s sitcoms,british t.v. sitcoms in the 80s,british tv sitcoms of the 80s,80s british family sitcoms,uk 80s sitcoms,80's uk sitcoms list,80s uk sitcom theme songs,80s uk comedy sitcoms,late 80s uk sitcoms,top 10 80's uk sitcoms",
            "thumbnails": {
                "default": {
                    "url": "https://i.ytimg.com/vi/UlOKNKLd99w/default.jpg",
                    "width": 120,
                    "height": 90,
                },
                "medium": {
                    "url": "https://i.ytimg.com/vi/UlOKNKLd99w/mqdefault.jpg",
                    "width": 320,
                    "height": 180,
                },
                "high": {
                    "url": "https://i.ytimg.com/vi/UlOKNKLd99w/hqdefault.jpg",
                    "width": 480,
                    "height": 360,
                },
                "standard": {
                    "url": "https://i.ytimg.com/vi/UlOKNKLd99w/sddefault.jpg",
                    "width": 640,
                    "height": 480,
                },
                "maxres": {
                    "url": "https://i.ytimg.com/vi/UlOKNKLd99w/maxresdefault.jpg",
                    "width": 1280,
                    "height": 720,
                },
            },
            "channelTitle": "70s tv, 80s tv and 90s tv - The Foot Of Our Stairs",
            "playlistId": "UUxn70TcSwA18B92Oy8yuA_Q",
            "position": 0,
            "resourceId": {"kind": "youtube#video", "videoId": "UlOKNKLd99w"},
            "videoOwnerChannelTitle": "70s tv, 80s tv and 90s tv - The Foot Of Our Stairs",
            "videoOwnerChannelId": "UCxn70TcSwA18B92Oy8yuA_Q",
        },
    }
    vxd = vidDict(item)
    assert "timestamp" in vxd
    assert vxd["timestamp"] == 1672585218
    assert vxd["videoId"] == "UlOKNKLd99w"
