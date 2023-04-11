import requests
from datetime import date, datetime, timezone
import logging
import time


BASE_URL = "https://zenodo.org"
FILE_NAME = "./investigations/zenodo-api/hits_unique_historic.json"
MAX_API_HITS = 10_000


def load_dataset_records(start:date, end: date):
    logging.info('Start loading datasets from Zenodo API')
    query = f'created:[{str(start)} TO {str(end)}]'
    logging.info(f"Loading for the following query: {query}")
    page = 1
    hits = []
    max_hits = 10_000
    while len(hits) < max_hits:
        params = {
            'q': query,
            'size': 1000,
            'sort': '-mostrecent',
            'all_versions': 'false',
            'page': page,
            'type': 'dataset'
        }
        r = requests.get(BASE_URL + "/api/records/", params=params)
        limit = int(r.headers['X-RateLimit-Limit'])
        remaining = int(r.headers['X-RateLimit-Remaining'])
        reset_time_utc = datetime.utcfromtimestamp(int(r.headers['X-RateLimit-Reset']))

        new_hits = r.json()['hits']['hits']
        hits += new_hits

        last_loaded_timestamp = new_hits[-1]['updated']
        last_loaded_timestamp = datetime.strptime(last_loaded_timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')

        total_hits = int(r.json()['hits']['total'])
        max_hits = total_hits if total_hits < max_hits else max_hits
        logging.info(f"Loaded page {page} collected {len(hits)}/{total_hits} datasets")
        logging.info(f"Remaining: {remaining}")


        if remaining == 0:
            current_time = datetime.now(timezone.utc)
            time_to_wait_in_seconds = (reset_time_utc - current_time).total_seconds()
            logging.info(f"Waiting for {time_to_wait_in_seconds} seconds")
            time.sleep(time_to_wait_in_seconds)

        page += 1

    return hits


# load_dataset_records(date(2022,10,1),date(2022,11,1))