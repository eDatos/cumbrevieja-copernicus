import shutil
from pathlib import Path

import settings
from copernicus import scrap


def test_links_available():
    vectors_url, pdf_url = scrap.get_links(1)
    assert (
        vectors_url == 'https://emergency.copernicus.eu/mapping/download/'
        '189298/EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3_vector.zip'
    )
    assert (
        pdf_url == 'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )


def test_links_not_available():
    vectors_url, pdf_url = scrap.get_links(7)
    assert vectors_url is None
    assert (
        pdf_url == 'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT07_r1_RTP02_v2.pdf'
    )


def test_monitoring_not_available():
    assert scrap.get_links(0) is None


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
