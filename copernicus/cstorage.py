from urllib.parse import urljoin

import requests
import settings
from logzero import logger


def set_value(key, value):
    logger.debug(f'Online key-value. Setting {key}: {value} ...')
    path = f'/set/{key}?value={value}'
    url = urljoin(settings.CUSTOM_KEYVALUE_API_URL, path)
    response = requests.get(url)
    data = response.json()
    return data['data'][key]['value']


def get_value(key, default=None, cast=str):
    logger.debug(f'Online key-value. Getting {key} ...')
    path = f'/get/{key}'
    url = urljoin(settings.CUSTOM_KEYVALUE_API_URL, path)
    response = requests.get(url)
    data = response.json()
    return cast(data['value']) if data else default
