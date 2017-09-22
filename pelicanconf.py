#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ross Fenning'
SITENAME = u'Traditional Mead UK'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DIRECT_TEMPLATES = ['index', 'categories']

THEME = './theme'
INDEX_SAVE_AS = 'blog.html'
SLUGIFY_SOURCE = 'basename'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'

CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'

TAG_URL = '{slug}/'
TAG_SAVE_AS = '{slug}/index.html'

CATEGORIES_SAVE_AS = 'producers/index.html'

AUTHOR_SAVE_AS = ''

MENUITEMS = (
    ('Home', '/'),
    ('Mead Producers', '/producers/'),
    ('What is mead?', '/what-is-mead/'),
    ('Types of Mead', '/types-of-mead/'),
    ('History of Mead', '/history-of-mead/'),
    ('Making Mead', '/making-mead/'),
)

DISPLAY_PAGES_ON_MENU=False
DISPLAY_TAGS_ON_MENU=False
DISPLAY_CATEGORIES_ON_MENU=False

PLUGINS = [
    'plugins.assets',
    'plugins.sitemap',
    'plugins.summary',
    'plugins.post_stats',
    'plugins.category_meta',
    'plugins.category_order',
    'plugins.pelican-open_graph',
    'plugins.filetime_from_git',
    'plugins.autopages',
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

TYPOGRIFY = True

STATIC_PATHS = ['images', 'extra/robots.txt', ]
EXTRA_PATH_METADATA = {
    'images': {'path': 'images'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

SHOW_STATS = True

CATEGORIES_ORDER_BY = 'size-rev'
TAGS_ORDER_BY = 'size-rev'
