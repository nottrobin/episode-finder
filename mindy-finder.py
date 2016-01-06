#!/usr/bin/env python

import requests
import json
import re
from feedgen.feed import FeedGenerator

response = requests.get('https://kat.cr/json.php?q=mindy+project+720', verify=False)
data = json.loads(response.text)

torrents = data['list']

latest_series = 0
latest_episode = 0
most_sources = 0
best_torrent = None

# Find the latest episode
for torrent in torrents:
    parts = re.search('S([0-9]{2})E([0-9]{2})', torrent['title'])

    if parts:
        torrent['series'] = int(parts.groups(1)[0])
        torrent['episode'] = int(parts.groups(1)[1])

        if torrent['series'] > latest_series:
            latest_series = torrent['series']

        if torrent['episode'] > latest_episode:
            latest_episode = torrent['episode']

# Find the best torrent of the latest episode
for torrent in torrents:
    if (
        "series" in torrent and "episode" in torrent and
        torrent['series'] == latest_series and
        torrent['episode'] == latest_episode
    ):
        torrent['sources'] = int(torrent['peers']) + int(torrent['seeds'])
        if torrent['sources'] >= most_sources:
            most_sources = torrent['sources']
            best_torrent = torrent

mindy_feed = FeedGenerator()
mindy_feed.title("Robin's Mindy feed")
mindy_feed.author({'name': 'Robin Winslow', 'email': 'robin@robinwinslow.uk'})
mindy_feed.description("The latest episode of The Mindy Project")
mindy_feed.link(href='http://vps.robinwinslow.co.uk/mindy-feed.rss')

mindy_episode = mindy_feed.add_entry()
mindy_episode.title(best_torrent['title'])
mindy_episode.link(href=best_torrent['torrentLink'])
mindy_episode.description(best_torrent['title'])

print mindy_feed.rss_str(pretty=True)

