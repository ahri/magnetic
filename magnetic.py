#!/usr/bin/env python

import sys
import re
import pyperclip
from lxml import html
from urllib import urlencode

PIRATE_BAY_SEARCH_FORMAT = "http://pirateproxy.ws/search/%s/0/99/0"
RESOLUTION = "720p"

def clip(text):
    pyperclip.copy(text)

if (len(sys.argv) < 2):
    print "Provide name and season ranges, e.g. 'Walking Dead' 1:1-12 2:3-5 3:6"
    sys.exit(1)

TITLE = sys.argv[1]

def range_execute(title, descriptor, per_episode):
    season, episode_range = descriptor.split(':')
    season = int(season)
    eps = episode_range.split('-')
    episodes = [int(eps[0])] if len(eps) == 1 else range(int(eps[0]), int(eps[1]) + 1)
    for ep in episodes:
        per_episode(title, season, ep)

def search(title, season, episode):
    query = "{title} s{season:0>2d}e{episode:0>2d} {resolution}".format(title=title, season=season, episode=episode, resolution=RESOLUTION)
    dom = html.parse(PIRATE_BAY_SEARCH_FORMAT % query)
    links = dom.xpath('//a[starts-with(@href, "magnet:")]')
    if len(links) == 0:
        print "ERROR: No results for query"
        return

    return links[0].get('href')

def copy_search_result(title, season, episode):
    magnet = search(title, season, episode)
    name = re.sub(r'[%&].*$', "", re.sub(r'^.*&dn=', "", magnet))
    clip(magnet)
    raw_input("magnet link for \"%s\"copied to clipboard, hit enter when done" % name)
    print

for arg in sys.argv[2:]:
    range_execute(TITLE, arg, copy_search_result)
