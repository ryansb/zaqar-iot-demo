from helpers import client

if __name__ == '__main__':
    scrape = client.queue('scrape')
    ingest = client.queue('ingest')
    complete = client.queue('completed')
    were_messages = True
    while were_messages:
        were_messages = False
        for msg in scrape.claim(ttl=60, grace=60):
            msg.delete()
            were_messages = True
        for msg in ingest.claim(ttl=60, grace=60):
            msg.delete()
            were_messages = True
        for msg in complete.claim(ttl=60, grace=60):
            msg.delete()
            were_messages = True
        print were_messages
