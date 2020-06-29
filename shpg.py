#!/usr/bin/env python3

"""Download items to ElasticSearch.

usage: shes.py -j JOB_ID [-h]

Download items from Scrapinhub cloud and upload them to ElasticSearch index.

optional arguments:
  -h, --help            show this help message and exit
  -j JOB_ID, --job_id JOB_ID                                Required Scrapy Cloud job idetentifier

"""
import os
from sqlalchemy import create_engine
from docopt import docopt
from scrapinghub import ScrapinghubClient
from pg_loader.pg_loader import PGPipeline

arguments = docopt(__doc__)

job_id = arguments.get('--job_id')

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
eng = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}')
api_key = os.environ.get('SH_APIKEY')
sc = ScrapinghubClient(api_key)
pg_pipe = PGPipeline(
    sc=sc,
    eng=eng,
    job_id=job_id,
).process_items()
