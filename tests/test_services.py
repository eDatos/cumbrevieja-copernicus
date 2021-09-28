import shutil

import settings
from copernicus import scrap, services


def test_extract_map_timemstamp():
    pdf_url = (
        'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )
    pdf_file = scrap.download_pdf(pdf_url, 1)
    map_timestamp = services.extract_map_timestamp(pdf_file)
    assert map_timestamp == ('21/09/2021 07:14 ' + settings.MAP_TIMESTAMP_TZ)
    shutil.rmtree(pdf_file.parent)
