from urllib.parse import urljoin

import requests

import settings


def set_value(key, value, namespace=settings.KEYVALUE_API_NAMESPACE):
    url = settings.KEYVALUE_API_SET_URL
    key = f'{namespace}-{key}'
    urlparts = [settings.KEYVALUE_API_TOKEN, key, str(value)]
    for urlpart in urlparts:
        url = urljoin(url, urlpart + '/')
    return requests.post(url).json()


def get_value(key, default=None, namespace=settings.KEYVALUE_API_NAMESPACE, cast=str):
    url = settings.KEYVALUE_API_GET_URL
    key = f'{namespace}-{key}'
    urlparts = [settings.KEYVALUE_API_TOKEN, key]
    for urlpart in urlparts:
        url = urljoin(url, urlpart + '/')
    return cast(value) if (value := requests.get(url).json()) else default
