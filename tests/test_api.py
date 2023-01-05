from ytsubs.api import getAuthService, getSubscriptions


def test_getAuthService():
    built = getAuthService()
    assert "googleapiclient.discovery.Resource" in str(built)


def test_getSubscriptions():
    ytauth = getAuthService()
    chans = getSubscriptions(ytauth)
    assert len(chans) > 0
