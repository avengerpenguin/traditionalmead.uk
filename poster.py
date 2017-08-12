#!/usr/bin/env python
import os
from collections import namedtuple
from lxml import etree
import facebook
import requests
from bs4 import BeautifulSoup
from iso8601 import iso8601
from datetime import datetime
import random


http = requests.Session()

sitemap = etree.parse('http://traditionalmead.uk/sitemap.xml')
ns = sitemap.getroot().nsmap[None]


urls = {
    url for url in sitemap.xpath('/s:urlset/s:url/s:loc/text()', namespaces={'s': ns})
    if '<meta property="og:type" content="article" />' in http.get(url).text
}


graph = facebook.GraphAPI(version='2.7')
token = graph.get_app_access_token('1405522322829296', os.getenv('FACEBOOK_APP_SECRET'))


graph = facebook.GraphAPI(access_token=token, version='2.7')
posts = graph.request(
    '/traditionalmeaduk/posts?fields=created_time,link&limit=100')['data']


last_post_time = iso8601.parse_date(posts[0]['created_time'])
print('Last posted at {t} ...'.format(t=last_post_time))
quiet_period = datetime.now(tz=last_post_time.tzinfo) - last_post_time
print('... which is {t} days ago'.format(t=quiet_period.days))


if random.randint(5, 9) <= quiet_period.days:

    print('I will post!')

    not_posted = urls - {post['link'] for post in posts if 'link' in post}

    articles = []
    for url in not_posted:
        soup = BeautifulSoup(http.get(url).content.decode('utf-8'), 'lxml')

        og_type_meta_tag = soup.find('meta', {'property': 'og:type'})

        if og_type_meta_tag and og_type_meta_tag['content'] == 'article':

            article = {
                'url': url,
            }

            og_desc_meta_tag = soup.find('meta', {'property': 'og:description'})

            if og_desc_meta_tag:
                article['description'] = og_desc_meta_tag['content']

            articles.append(article)

    article_to_post = random.choice(articles)

    print(graph.request('/traditionalmeaduk/feed', post_args={
        'link': article['url'],
        'message': article['description'],
    }))