import glob
import os
import re
from datetime import datetime
from pathlib import Path

import PyPDF2
import settings
from logzero import logger
from pytz import timezone


def rename_newest_file(new_file: Path) -> Path:
    '''Rename the newest (last-modified) file from the folder of new_file
    with the name of new_file'''
    folder = new_file.parent
    extension = f'*{new_file.suffix}'
    list_of_files = glob.glob(str(folder / extension))
    newest_file = max(list_of_files, key=os.path.getctime)
    return Path(newest_file).rename(new_file)


def extract_map_timestamp(pdf_file: Path) -> datetime:
    '''Return the scrapped map timestamp from pdf file (UTC)'''
    logger.debug('Extracting map timestamp...')
    pdf_reader = PyPDF2.PdfFileReader(str(pdf_file))
    page = pdf_reader.getPage(0)
    text = page.extractText()
    if s := re.search(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})ActivationMap', text):
        map_timestamp = datetime.strptime(s.groups()[0], '%d/%m/%Y %H:%M')
        return map_timestamp.replace(tzinfo=timezone(settings.MAP_TIMESTAMP_TZ))


def build_vectors_filename(target_monitoring_id: str, map_timestamp: datetime):
    buf = []
    buf.append(map_timestamp.strftime('%Y%m%d_%H%M_%Z'))
    buf.append(settings.COPERNICUS_COMPONENT_ID)
    buf.append(f'M{target_monitoring_id}.zip')
    return '-'.join(buf)
