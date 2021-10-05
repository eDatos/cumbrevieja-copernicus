import shutil

import settings
from copernicus import scrap, services


def test_extract_map_timemstamp(map_timestamp_m1):
    pdf_url = (
        'https://emergency.copernicus.eu/mapping/system/files/components/'
        'EMSR546_AOI01_GRA_MONIT01_r1_RTP02_v3.pdf'
    )
    pdf_file = scrap.download_pdf(pdf_url, 1)
    map_timestamp_to_be_checked = services.extract_map_timestamp(pdf_file)
    assert map_timestamp_m1 == map_timestamp_to_be_checked
    shutil.rmtree(pdf_file.parent)


def test_build_vectors_filename(map_timestamp_m1):
    vectors_filename_to_be_checked = services.build_vectors_filename(1, map_timestamp_m1)
    component_id = settings.COPERNICUS_COMPONENT_ID
    vectors_filename = f'20210921_0714_UTC-{component_id}-M1.zip'
    assert vectors_filename == vectors_filename_to_be_checked
