#!/usr/bin/env python
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

print("digraph g {")
print("\tnode[shape=circle];")


urls = {
    "http://traditionalmead.uk/",
    "http://traditionalmead.uk/what-is-mead/",
    "http://traditionalmead.uk/types-of-mead/",
    "http://traditionalmead.uk/english-meads/",
}
paths = set()
http = requests.Session()


def fetch(fetch_url, name_from):
    print(f"Fetching {fetch_url}...", file=sys.stderr)
    r = http.get(fetch_url)
    soup = BeautifulSoup(r.text, "html5lib")

    urls_to_fetch = {}

    if name_from == "home":
        links = soup.find("nav").find_all("a")
    else:
        links = soup.find("main").find_all("a")

    for link in links:
        if link["href"]:
            url = urljoin("http://traditionalmead.uk/", link["href"])

            if "http://traditionalmead.uk/" in url:
                name_to = str(url).replace("http://traditionalmead.uk/", "").rstrip("/")
            else:
                name_to = urlparse(url)[1]  # Hostname

            if name_to in [
                "disqus.com",
                "www.pinterest.com",
                "types-of-mead",
                "metheglin-spiced-mead",
                "scottish-meads",
                "english-meads",
                "cyser",
                "craft-mead",
                "pure-honey-mead",
                "mead-liqueurs",
                "chouchen",
                "sparkling",
                "dry-meads",
                "pyment",
                "treacle",
                "christmas-meads",
            ]:
                continue

            if name_to:
                if not (name_from, name_to) in paths:
                    print(f'\t"{name_from}" -> "{name_to}";')
                    paths.add((name_from, name_to))

                if "http://traditionalmead.uk/" in url and url not in urls:
                    print(f"Queueing {fetch_url}...", file=sys.stderr)
                    urls_to_fetch[name_to] = url
                    urls.add(url)

    for name in urls_to_fetch:
        fetch(urls_to_fetch[name], name)


fetch("http://traditionalmead.uk/", "home")


print("}")
