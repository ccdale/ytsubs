from ytsubs.api import getAuthService, getSubscriptions


def test_getAuthService():
    built = getAuthService()
    assert "googleapiclient.discovery.Resource" in str(built)


def test_getSubscriptions():
    chans = getSubscriptions()
    assert len(chans) > 0
