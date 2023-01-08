# ytsubs

A python application designed to run as the target of a cron event to download
the latest subscribed Youtube videos.

## install code
Clone this repository and use [poetry](https://python-poetry.org/) to install
the python code.

```
git clone https://github.com/ccdale/ytsubs.git
cd ytsubs
poetry install
```

## install application

Build a python wheel using

```
rm -rf dist
poetry build
```

You can now install the wheel using the usual pip mechanism

```
python -m pip install dist/ytsubs*whl --user --upgrade
```

If you change the code increase the version number in `pyproject.toml`,
`src/ytsubs/__init__.py` and `tests/test_ytsubs.py` and then re-run the above
command

You should now have 2 new commands `getvids` and `getplaylist` - see below for
how to use them.

## credentials

You'll need Google Youtube API credentials to run this application.  Go to
https://developers.google.com/youtube/v3/getting-started and follow the first 3
steps to create an application. Credentials should be stored (as a json file) in
the `$XDG_CONFIG_HOME` directory (normally `$HOME/.config/ytsubs`).

If this directory doesn't exist this app will create it, direct you back here
and then exit.

This app will look for `$XDG_CONFIG_HOME/ytsubs/ytsubs-client.json` - so this is
the file name that you should save the Youtube API credentials file that Google
created for you.

The final step is to authorise this application to use your Youtube account.
Hopefully when this is necessary the OAuth2 library will hold your hand and tell
you what to do (and in some cases even open a browser to the correct
authorisation page :-)

## Usage

`getvids` is designed to be used from cron every 24 hours, it'll look for it's
credentials and session files in the config directory discussed above.  It asks
Youtube for a list of your subscriptions then for each of those it checks to see
if there are any videos newer than 24 hours ago. If there are it'll download
them to the output directory.  It'll also create `.nfo` files for Kodi to use
with the meta information about each video.
