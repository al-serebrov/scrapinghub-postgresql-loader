import logging
from typing import Iterable
import os
from sqlalchemy import (
    Boolean, Column, DateTime, Float, Integer, String
)
import datetime
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger('pg_loader')
logger.setLevel(level=logging.DEBUG)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# add formatter to console and file handlers
ch.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)


Base = declarative_base()


class PGPipeline(object):
    def __init__(self, sc, eng, job_id):
        self.eng = eng
        self.sc = sc
        self.job_id = job_id
        self.table_name = self.job_id.replace('/', '_')

    def _get_items(self) -> Iterable:
        """Get items from Scrapy Cloud.

        Besides getting items this method also gets job metadata,
        extracts items count and calls method to calculate buffer size.

        Returns:
            items - an iterator with items.

        Raises:
            ValueError - if the method is unable to get items count.
        """
        job = self.sc.get_job(self.job_id)
        metadata = job.metadata.list()

        items_count = 0
        for data in metadata:
            if data[0] == 'scrapystats':
                items_count = data[1]['item_scraped_count']

        if not items_count:
            raise ValueError('Unable to get items count for job stats')

        logger.debug(
            'There are {} items scraped. Downloading...'.format(items_count)
        )
        items = job.items.list()
        return items

    def process_items(self):
        data_df = pd.DataFrame(self._get_items())
        data_df = data_df.astype(str)
        data_df.to_sql(
            self.table_name,
            con=self.eng,
            index=True,
            index_label='id',
            if_exists='replace')
