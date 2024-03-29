#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://traditionalmead.uk'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""


#GOOGLE_ANALYTICS_ID = 'UA-80839950-4'
DISQUS_SITE = 'traditionalmead'
GOOGLE_TAG_ID = 'G-L13NCF579B'
GOOGLE_ADSENSE_ID = 'ca-pub-7863038150136152'

SHOW_STATS=False
