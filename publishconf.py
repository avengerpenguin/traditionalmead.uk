#!/usr/bin/env python

import os
import sys

from pelicanconf import *  # noqa

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.


sys.path.append(os.curdir)

SITEURL = "https://traditionalmead.uk"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""


DISQUS_SITE = "traditionalmead"
GA4_MEASUREMENT_ID = "G-L13NCF579B"
# Works with a certified IAB TCF CMP (for example, a published AdSense
# Privacy & messaging European regulations message). This is not the CMP.
GOOGLE_TCF_CONSENT_MODE = True
AFFILIATE_RULES = [
    {
        "domain": "amazon.co.uk",
        "query_parameter": "tag",
        "network": "amazon",
    },
    {"domain": "amzn.to", "network": "amazon"},
    {"domain": "awin1.com", "network": "awin"},
    {"domain": "go.adt253.net", "network": "adtraction"},
]
GOOGLE_ADSENSE_ID = "ca-pub-7863038150136152"

SHOW_STATS = False
