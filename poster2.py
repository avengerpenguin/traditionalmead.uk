#!/usr/bin/env python
import os
import random
from datetime import datetime
from urllib import parse as urlparse

import facebook
import oauth2 as oauth
import requests
from bs4 import BeautifulSoup
from iso8601 import iso8601
from lxml import etree

http = requests.Session()

sitemap = etree.parse("http://traditionalmead.uk/sitemap.xml")
ns = sitemap.getroot().nsmap[None]


urls = {
    url
    for url in sitemap.xpath("/s:urlset/s:url/s:loc/text()", namespaces={"s": ns})
    if '<meta property="og:type" content="article" />' in http.get(url).text
}

graph = facebook.GraphAPI(version="2.7")
token = graph.get_app_access_token(
    "1405522322829296", os.getenv("FACEBOOK_CLIENT_TOKEN")
)
token = "EAATZBUKrGrZCABAFHQlFfjn8lSR4eE2aGzQ7MKkVGGfqkukZB8sna7Ka8dtVLoozullSlEODDZBE2fPZCiwzcad8siawCPkM1mTD9lYvEaZBDZCVu8DyMJXi7Wjx2g15RAIW9Y1ZAZBm4wFl4fZBBZCN7GfuvfZCofawUqCKjQuw7nALqP9FAlgwKViKqk2m1ihcfbMZD"

print(token)


graph = facebook.GraphAPI(version="2.7", access_token=token)
posts = graph.request("/traditionalmeaduk/posts?fields=created_time,link&limit=100")[
    "data"
]


last_post_time = iso8601.parse_date(posts[0]["created_time"])
print(f"Last posted at {last_post_time} ...")
quiet_period = datetime.now(tz=last_post_time.tzinfo) - last_post_time
print(f"... which is {quiet_period.days} days ago")


if True or random.randint(3, 10) <= quiet_period.days:

    print("I will post!")

    not_posted = urls - {post["link"] for post in posts if "link" in post}

    articles = []
    for url in not_posted:
        soup = BeautifulSoup(http.get(url).content.decode("utf-8"), "lxml")

        og_type_meta_tag = soup.find("meta", {"property": "og:type"})

        if og_type_meta_tag and og_type_meta_tag["content"] == "article":

            article = {
                "url": url,
            }

            for meta_tag in soup.find_all("meta"):
                if "property" in meta_tag.attrs and "og:" in meta_tag["property"]:
                    article[meta_tag["property"].split(":")[1]] = meta_tag["content"]

            first_img_tag = soup.find("div", class_="entry-content").find("img")
            if first_img_tag:
                article["image"] = urlparse.urljoin(
                    "http://traditionalmead.uk/", first_img_tag["src"]
                )

            articles.append(article)

    article_to_post = random.choice(articles)
    if len(article_to_post["description"]) > 140:
        article_to_post["text"] = article_to_post["description"][:139] + "…"
    else:
        article_to_post["text"] = article_to_post["description"]

    print(article_to_post)

    consumer = oauth.Consumer(
        key="599b51694409551417438196", secret=os.getenv("BUFFER_CLIENT_SECRET")
    )
    request_token_url = "https://bufferapp.com/oauth2/authorize"

    print(
        http.post(
            "https://api.bufferapp.com/1/updates/create.json",
            data=[
                ("access_token", os.getenv("BUFFER_ACCESS_TOKEN")),
                ("shorten", "true"),
                ("text", article_to_post["text"]),
                ("profile_ids[]", "58b966e68aaa5dab472ec886"),
                ("profile_ids[]", "58b966908aaa5db14a2ec887"),
                ("media[link]", article_to_post["url"]),
                ("media[title]", article_to_post["title"]),
                ("media[picture]", article_to_post["image"]),
                ("media[description]", article_to_post["description"]),
            ],
        ).text
    )

    # user = client.user()
    # user.create_update(article_to_post['description'], [
    #     "58b966e68aaa5dab472ec886",
    #     "58b966908aaa5db14a2ec887"
    # ], options={
    #     'body': {
    #         'media': {
    #             'link': article_to_post['url'],
    #             'title': article_to_post['title'],
    #             'picture': article_to_post['image'],
    #         }
    #     }
    # })
