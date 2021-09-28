import shutil
from pathlib import Path

import pytest
import settings
from bs4.element import Tag
from copernicus import scrap


@pytest.fixture
def products():
    return list(scrap.get_products())


def test_get_products(products):
    assert len(products) > 1
    for product, monitoring_id in products:
        assert type(product) == Tag
        assert type(monitoring_id) == int
        assert monitoring_id >= 0


def test_links_available(products):
    # [EMSR546] La Palma: Grading Product, Monitoring 1, version 3, release 1, RTP Map #02
    product, monitoring_id = products[9]
    assert monitoring_id == 1
    vectors_url, pdf_url = scrap.get_links(product)
    assert (
        vectors_url == 'https://emergency.copernicus.eu/mapping/download/'
        '189298/EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3_vector.zip'
    )
    assert (
        pdf_url == 'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )


def test_links_not_available(products):
    # [EMSR546] La Palma: Grading Product, Monitoring 7, version 2, release 1, RTP Map #02
    product, monitoring_id = products[3]
    assert monitoring_id == 7
    vectors_url, pdf_url = scrap.get_links(product)
    assert vectors_url is None
    assert (
        pdf_url == 'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT07_r1_RTP02_v2.pdf'
    )


def test_download_vectors():
    url = (
        'https://emergency.copernicus.eu/mapping/download/'
        '189298/EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3_vector.zip'
    )
    scrap.download_vectors(url, 1)
    f = Path(settings.DOWNLOADS_DIR / 'EMSR546-M1.zip')
    assert f.exists()
    shutil.rmtree(f.parent)


def test_download_pdf():
    url = (
        'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )
    scrap.download_pdf(url, 1)
    f = Path(settings.DOWNLOADS_DIR / 'EMSR546-M1.pdf')
    assert f.exists()
    shutil.rmtree(f.parent)
