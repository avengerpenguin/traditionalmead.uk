# AUTHOR = u'Ross Fenning'
# SITEURL = ''
#
# PATH = 'content'
#
# TIMEZONE = 'Europe/London'
#
# DEFAULT_LANG = u'en'
#
# # Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# DEFAULT_PAGINATION = False
#
# # Uncomment following line if you want document-relative URLs when developing
# #RELATIVE_URLS = True
#
# DIRECT_TEMPLATES = ['index', 'categories']
#
# INDEX_SAVE_AS = 'blog.html'
# SLUGIFY_SOURCE = 'basename'
#
# PAGE_URL = '{slug}/'
# PAGE_SAVE_AS = '{slug}/index.html'
#
# ARTICLE_URL = '{slug}/'
# ARTICLE_SAVE_AS = '{slug}/index.html'
#
# CATEGORY_URL = '{slug}/'
# CATEGORY_SAVE_AS = '{slug}/index.html'
#
# TAG_URL = '{slug}/'
# TAG_SAVE_AS = '{slug}/index.html'
#
# CATEGORIES_SAVE_AS = 'producers/index.html'
# CATEGORIES_TITLE = 'Mead Producers in the UK and Europe'
#
# DISPLAY_PAGES_ON_MENU=False
# DISPLAY_TAGS_ON_MENU=False
# DISPLAY_CATEGORIES_ON_MENU=False
#
# SITEMAP = {
#     'format': 'xml',
#     'priorities': {
#         'articles': 0.5,
#         'indexes': 0.5,
#         'pages': 0.5
#     },
#     'changefreqs': {
#         'articles': 'monthly',
#         'indexes': 'daily',
#         'pages': 'monthly'
#     }
# }
#
# TYPOGRIFY = True
#
# # STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/ads.txt', 'icon']
# # EXTRA_PATH_METADATA = {
# #     'images': {'path': 'images'},
# #     'icon/favicon.ico': {'path': 'favicon.ico'},
# #     'extra/robots.txt': {'path': 'robots.txt'},
# #     'extra/ads.txt': {'path': 'ads.txt'},
# # }
#
#
# SHOW_STATS = True
#
# CATEGORIES_ORDER_BY = 'size-rev'
# TAGS_ORDER_BY = 'size-rev'
#

from voltaire.pelican import *

SITENAME = "Traditional Mead UK"
AUTHOR = "Ross Fenning"
STATIC_PATHS += ["icon", "images"]
FILENAME_METADATA = "(?P<title>.*)"


PATH = "Mead"
PAGE_PATHS = ["."]
ARTICLE_PATHS = []


PLUGINS += ["voltaire.search"]
TEMPLATE_PAGES = {
    "search.html": "search/index.html",
}

STATIC_PATHS += ["extra/images", "extra/icons", "extra/ads.txt"]
EXTRA_PATH_METADATA = {
    "extra/ads.txt": {"path": "ads.txt"},
}
#
# EXTRA_PATH_METADATA = {
#     "extra/CNAME": {"path": "CNAME"},
#     'images': {'path': 'images'},
# }

# PLUGINS += [
#     'plugins.assets',
#     'plugins.sitemap',
#     'plugins.summary',
#     'plugins.post_stats',
#     'plugins.category_meta',
#     'plugins.category_order',
#     'plugins.pelican-open_graph',
#    'plugins.filetime_from_git',
#     'plugins.autopages',
# ]

MENUITEMS_START = (
    ("Home", "/"),
    ("Mead Producers", "/producers/"),
    ("What is mead?", "/what-is-mead/"),
    ("Types of Mead", "/types-of-mead/"),
    ("History of Mead", "/history-of-mead/"),
    ("Making Mead", "/making-mead/"),
    ("Search", "/search/"),
)
# THEME = './theme'
