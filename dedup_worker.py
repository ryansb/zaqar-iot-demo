# Pull URL
# Strip query string
# Query exists
# IFN save to sqlite
# IFN push to queue
# IFY do nothing

seen = {}

if __name__ == '__main__':
    from helpers import client
    ingest = client.queue('ingest')
    scrape = client.queue('scrape')

    while True:
        claimed = ingest.claim(ttl=180, grace=60)
        send = []
        for msg in claimed:
            msg.delete()
            if seen.get(msg.body):
                print "skipping %s, seen %d pages" % (msg.body, len(seen.keys()))
                continue
            print "Sending along %s" % msg.body
            seen[msg.body] = True
            send.append({'body': msg.body, 'ttl': 180})

        if len(send): scrape.post(send)
