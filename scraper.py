# 1. Claim a message
# 2. Grab HTML
# 3. Delete message
# 4. Push more URLs
from bs4 import BeautifulSoup
import sys
from helpers import client
import requests
import urlparse

def scrape_generator(url):
    parent = urlparse.urlsplit(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in soup.findAll('a'):
        link = tag.get('href')

        if '#' in link:
            link = ''.join(link.split('#')[:-1])

        if link.startswith('mailto:'):
            continue
        elif urlparse.urlsplit(link).scheme in ('http', 'https'):
            yield link
        elif link.startswith('/'):
            yield parent.scheme + '://' + parent.netloc + link
        elif parent.path.endswith('/'):
            yield parent.scheme + '://' + parent.netloc + parent.path + link
        else:
            yield parent.scheme + '://' + parent.netloc + parent.path + '/' + link


seen = {}
def scrapable(uri):
    if not uri.startswith(sys.argv[1]):
        return False
    if seen.get(uri):
        return False
    seen[uri] = True
    return True


if __name__ == '__main__':
    scrape = client.queue('scrape')
    ingest = client.queue('ingest')
    complete = client.queue('completed')

    while True:
        claimed = scrape.claim(ttl=180, grace=60, limit=1)
        for msg in claimed:
            messages = [
                {'body': u, 'ttl': 180}
                for u in scrape_generator(msg.body)
                if scrapable(u)
            ]
            if len(messages):
                ingest.post(messages)
            complete.post({'body': msg.body, 'ttl': 300})
            msg.delete()
