from ytsubs import __appname__, __version__
from ytsubs.auth import credsFiles, authService


def test_credsFiles():
    clientfn, sessionfn = credsFiles()
    assert str(clientfn).endswith(f"{__appname__}-client.json")
    assert str(sessionfn).endswith(f"{__appname__}-session.json")


def test_authService():
    creds = authService()
    assert creds.invalid is False
    assert creds.client_id.endswith("apps.googleusercontent.com")
