import shutil
from pathlib import Path

import settings
from bs4.element import Tag
from copernicus import scrap


def test_get_products(products):
    assert len(products) > 1
    for product, monitoring_id in products:
        assert type(product) == Tag
        assert type(monitoring_id) == int
        assert monitoring_id >= 0


def test_links_available(products):
    # [EMSR546] La Palma: Grading Product, Monitoring 1, version 3, release 1, RTP Map #02
    for product, monitoring_id in products:
        if monitoring_id == 1:
            vectors_url, pdf_url = scrap.get_links(product)
            assert (
                vectors_url == 'https://emergency.copernicus.eu/mapping/download/'
                '189298/EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3_vector.zip'
            )
            assert (
                pdf_url
                == 'https://emergency.copernicus.eu/mapping/system/files/components/'
                'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
            )
            break


def test_links_not_available(products):
    # [EMSR546] La Palma: Grading Product, Monitoring 7, version 2, release 1, RTP Map #02
    for product, monitoring_id in products:
        if monitoring_id == 7:
            vectors_url, pdf_url = scrap.get_links(product)
            assert vectors_url is None
            assert (
                pdf_url
                == 'https://emergency.copernicus.eu/mapping/system/files/components/'
                'EMSR546_AOI01_GRA_MONIT07_r1_RTP02_v2.pdf'
            )
            break


def test_download_vectors(map_timestamp_m1):
    url = (
        'https://emergency.copernicus.eu/mapping/download/'
        '189298/EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3_vector.zip'
    )
    scrap.download_vectors(url, 1, map_timestamp_m1)
    component_id = settings.COPERNICUS_COMPONENT_ID
    filename = f'20210921_0714_UTC-{component_id}-M1.zip'
    f = Path(settings.DOWNLOADS_DIR / filename)
    assert f.exists()
    shutil.rmtree(f.parent)


def test_download_pdf():
    url = (
        'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )
    scrap.download_pdf(url, 1)
    component_id = settings.COPERNICUS_COMPONENT_ID
    filename = f'{component_id}-M1.pdf'
    f = Path(settings.DOWNLOADS_DIR / filename)
    assert f.exists()
    shutil.rmtree(f.parent)
