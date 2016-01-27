# 1. take a URL from the CLI
# 2. Push to zaqar
# 3. Listen on `collected` queue and print
import sys
import datetime
from helpers import client

if __name__ == '__main__':
    q = client.queue('ingest')

    q.post({'body': sys.argv[1], 'ttl': 300})

    complete = client.queue('completed')
    while True:
        claimed = complete.claim(ttl=180)
        for msg in claimed:
            print "%s %s" % (datetime.datetime.now(), msg.body)
            msg.delete()
