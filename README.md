# ytsubs

A python application designed to run as the target of a cron event to download
the latest subscribed youtube videos.

## install
Clone this repository and use [poetry](https://python-poetry.org/) to install
the python code.

```
git clone https://github.com/ccdale/ytsubs.git
cd ytsubs
poetry install
```

## credentials

You'll need Google Youtube API credentials to run this application.  Go to
https://developers.google.com/youtube/v3/getting-started and follow the first 3
steps to create an application.
