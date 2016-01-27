from helpers import client

if __name__ == '__main__':
    scrape = client.queue('scrape')
    ingest = client.queue('ingest')
    complete = client.queue('completed')

    were_messages = True

    while were_messages:
        were_messages = False
        for q in (scrape, ingest, complete):
            for msg in q.claim(ttl=60, grace=60, limit=20):
                msg.delete()
                were_messages = True
