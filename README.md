1. Push starting URL to ingest
1. Wait for workers to finish (reader topic has nothing in it)

```
ingest topic -> deduplication worker -> scrape topic -> pull worker -> scraped URLs to completed topic
                                                          \-> found URLs to ingest topic
```
