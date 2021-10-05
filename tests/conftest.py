import datetime

import pytest
import pytz
import settings
from copernicus import scrap


@pytest.fixture
def products(scope='module'):
    return list(scrap.get_products())


@pytest.fixture
def map_timestamp_m1(scope='module'):
    '''Map timestamp for Monitoring 1'''
    return datetime.datetime(
        day=21,
        month=9,
        year=2021,
        hour=7,
        minute=14,
        tzinfo=pytz.timezone(settings.MAP_TIMESTAMP_TZ),
    )
