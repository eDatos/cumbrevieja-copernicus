from urllib.parse import urljoin

import requests
from logzero import logger

import settings


def set_value(key, value, namespace=settings.KEYVALUE_API_NAMESPACE):
    logger.debug(f'Online key-value. Setting {key}: {value} ...')
    url = settings.KEYVALUE_API_SET_URL
    key = f'{namespace}-{key}'
    urlparts = [settings.KEYVALUE_API_TOKEN, key, str(value)]
    for urlpart in urlparts:
        url = urljoin(url, urlpart + '/')
    return requests.post(url).json()


def get_value(key, default=None, namespace=settings.KEYVALUE_API_NAMESPACE, cast=str):
    logger.debug(f'Online key-value. Getting {key} ...')
    url = settings.KEYVALUE_API_GET_URL
    key = f'{namespace}-{key}'
    urlparts = [settings.KEYVALUE_API_TOKEN, key]
    for urlpart in urlparts:
        url = urljoin(url, urlpart + '/')
    return cast(value) if (value := requests.get(url).json()) else default
