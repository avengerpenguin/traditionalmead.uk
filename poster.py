#!/usr/bin/env python
import asyncio
import os
import random
import time
import clize
from lxml import etree
import requests
from bs4 import BeautifulSoup
from urllib import parse as urlparse
from functools import partial
from collections import namedtuple
import aiohttp
import urllib.parse
from yarl import URL


class AsyncHttpApi(object):
    def __init__(self, aiohttp_session, base_url):
        self.http = aiohttp_session
        self.base_url = base_url

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return self
        else:
            new_url = self.base_url + '/' + '/'.join(args)
            return self.__class__(self.http, new_url)

    def __getattr__(self, key):
        if key in ['put', 'get', 'post', 'delete']:
            requests_verb = getattr(self.http, key)
            return partial(requests_verb, self.base_url)
        else:
            new_url = self.base_url + '/'  + key
            return self.__class__(self.http, new_url)


Article = namedtuple('Article', ['title', 'url', 'image', 'description'])


async def articles_from_urls(urls):
    async with aiohttp.ClientSession() as session:
        futures = [session.get(url) for url in urls]

        for future in futures:
            async with future as response:
                soup = BeautifulSoup(await response.text(), 'lxml')

                metadata = {}
                for meta_tag in soup.find_all('meta'):
                    if 'property' in meta_tag.attrs and 'og:' in meta_tag['property']:
                        metadata[meta_tag['property'].split(':')[1]] = meta_tag['content']

                if metadata.get('type') == 'article':
                    first_img_tag = soup.find('div', class_='entry-content').find('img')
                    if first_img_tag:
                        metadata['image'] = urlparse.urljoin(
                            'http://traditionalmead.uk/', first_img_tag['src'])

                    article = Article(title=metadata['title'],
                                      url=response.url,
                                      image=metadata.get('image', None),
                                      description=metadata['description'])
                    yield article


async def get_all_articles(website_url):
    sitemap = etree.parse(str(URL(website_url).with_path('/sitemap.xml')))
    ns = sitemap.getroot().nsmap[None]

    urls = sitemap.xpath('/s:urlset/s:url/s:loc/text()', namespaces={'s': ns})

    articles = set()
    async for article in articles_from_urls(urls):
        articles.add(article)
    return articles


async def get_buffer_articles(website_url, profile_ids, status='sent'):
    async with aiohttp.ClientSession() as session:
        buffer = AsyncHttpApi(session, 'https://api.bufferapp.com/1')
        futures = [buffer.profiles(profile_id).updates(status + '.json').get(params={'access_token': os.getenv('BUFFER_ACCESS_TOKEN'), 'count': 100})
                   for profile_id in profile_ids]

        articles = set()

        for future in futures:
            async with future as response:
                response_json = await response.json()
                links = []
                for update in response_json['updates']:
                    try:
                        link = update['media']['link']
                        async with session.get(link) as response:
                            if response.url.host + response.url.path == 'www.facebook.com/flx/warn/':
                                link = str(URL(response.url.query['u']).with_query(None))
                            else:
                                link = str(response.url.with_query(None))
                        if link.startswith(website_url):
                            links.append(link)
                    except KeyError:
                        continue
                async for article in articles_from_urls(links):
                    articles.add(article)

        return articles


async def queue(articles_to_post, profile_ids):
    async with aiohttp.ClientSession() as session:
        buffer = AsyncHttpApi(session, 'https://api.bufferapp.com/1')
        futures = []
        for article_to_post in articles_to_post:

            if len(article_to_post.description) > 140:
                article_text = article_to_post.description[:139] + '…'
            else:
                article_text = article_to_post.description

            data=[
                ('access_token', os.getenv('BUFFER_ACCESS_TOKEN')),
                ('shorten', 'true'),
                ('text', article_text),
                ('media[link]', article_to_post.url),
                ('media[title]', article_to_post.title),
                ('media[picture]', article_to_post.image),
                ('media[description]', article_to_post.description)
            ]
            for profile_id in profile_ids:
                data.append(('profile_ids[]', profile_id))
                futures.append(buffer.updates('create.json').post(data=data))

        for future in futures:
            async with future as response:
                print(await response.text())

        futures = []
        for profile_id in profile_ids:
            futures.append(buffer.profiles(profile_id).updates('shuffle.json').post(data={'access_token': os.getenv('BUFFER_ACCESS_TOKEN')}))

        for future in futures:
            async with future as response:
                print(await response.text())


async def fillup(website_url, profile_ids):
    all_articles = await get_all_articles(website_url)
    articles_posted = await get_buffer_articles(website_url, profile_ids, status='sent')
    articles_queued = await get_buffer_articles(website_url, profile_ids, status='pending')

    unposted_articles = all_articles - articles_posted - articles_queued
    to_post = max(10 - len(articles_queued), 0)

    if to_post:
        articles_to_post = random.choices(list(unposted_articles), k=to_post)
        await queue(articles_to_post, profile_ids)

    # if unposted_articles:
    #     article_to_post = random.choice(unposted_articles)
    # else:
    #     raise NotImplemented
    # queue(article_to_post)


def main(website_url, profile_ids):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fillup(website_url, profile_ids.split(',')))
    finally:
        loop.close()


if __name__ == '__main__':
    clize.run(main)