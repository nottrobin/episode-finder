Episode finder
===

A utility to search for torrents on Kickass Torrents,
and generate an RSS feed of the best torrents with the following criteria:

- Return torrents in episode order, latest first
- Remove all but the best torrent for each episode
- Don't include torrents with less than 30 sources

This RSS feed is then intended to be fed into [DownloadStation](https://help.synology.com/dsm/?section=DownloadStation).

Dependencies
---

Install all python dependencies with pip:

``` bash
pip install -r requirements.txt
```

*Note:* on Debian systems, some extra dependencies are often needed to run [lxml](https://pypi.python.org/pypi/lxml).
You may need to install these system dependencies before running `pip install` again:

``` bash
apt-get install libxml2-dev libxslt1-dev python-dev
```

Usage
---

Run from the command-line:

``` bash
./episode-finder.py "mindy+project+720"  # RSS is output to STDOUT
```

Or run the server:

``` bash
./server.py
```

Now you can visit the server in a browser, e.g.: <http://127.0.0.1:8111/?q=mindy+project+720>.

