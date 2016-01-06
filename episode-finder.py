#!/usr/bin/env python

# Core
import json
import re
import sys

# Modules
import requests
from feedgen.feed import FeedGenerator

query = sys.argv[1]
if not query:
    print "Please provide a query to search for episode torrents"
    sys.exit()

kat_domains = [
    'https://kat.cr',
    'https://kat.al',
    'http://kat.asia',
    'http://kattorrents.in',
    'http://kickasstorrentcr.com'
]

for domain in kat_domains:
    try:
        response = requests.get(domain + '/json.php?q=' + query, verify=False)
        break
    except:
        continue

data = json.loads(response.text)

torrents = data['list']
episodes = []
valid_torrents = []
sorted_torrents = []
best_torrents = []
latest_series = 0
latest_episode = 0
most_sources = 0
sources_threshold = 30
best_torrent = None

# Find episodes and series for torrents
for torrent in torrents:
    parts = re.search('S([0-9]+)E([0-9]+)', torrent['title'])

    if parts:
        series = int(parts.groups(1)[0])
        episode = int(parts.groups(1)[1])
        episode_id = series * 1000 + episode
        torrent['episode_id'] = episode_id
        torrent['sources'] = int(torrent['peers']) + int(torrent['seeds'])
        if episode_id not in episodes:
            episodes.append(episode_id)
        valid_torrents.append(torrent)

# Put torrents in episode order
sorted_torrents = sorted(valid_torrents, key=lambda x: (x['episode_id'], x['sources']), reverse=True)

# Find the best torrent for each episode
for episode_id in sorted(episodes, reverse=True):
    top_torrent = [torrent for torrent in sorted_torrents if torrent['episode_id'] == episode_id][0]

    if top_torrent['sources'] > sources_threshold:
        best_torrents.append(top_torrent)

# Generate RSS feed
title = "Auto-generated episode feed for: " + query
mindy_feed = FeedGenerator()
mindy_feed.title(title)
mindy_feed.author({'name': 'Robin Winslow', 'email': 'robin@robinwinslow.uk'})
mindy_feed.description(title)
mindy_feed.link(href="http://example.com/")

for torrent in best_torrents:
    mindy_episode = mindy_feed.add_entry()
    mindy_episode.title(torrent['title'])
    mindy_episode.link(href=torrent['torrentLink'])
    mindy_episode.description(torrent['title'])

print mindy_feed.rss_str(pretty=True)

