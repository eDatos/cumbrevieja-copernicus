import glob
import os
import re
from pathlib import Path

import PyPDF2
import settings


def rename_newest_file(new_file: Path) -> Path:
    '''Rename the newest (last-modified) file from the folder of new_file
    with the name of new_file'''
    folder = new_file.parent
    extension = f'*{new_file.suffix}'
    list_of_files = glob.glob(str(folder / extension))
    newest_file = max(list_of_files, key=os.path.getctime)
    return Path(newest_file).rename(new_file)


def extract_map_timestamp(pdf_file: Path) -> str:
    pdf_reader = PyPDF2.PdfFileReader(str(pdf_file))
    page = pdf_reader.getPage(0)
    text = page.extractText()
    if s := re.search(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})ActivationMap', text):
        return f'{s.groups()[0]} {settings.MAP_TIMESTAMP_TZ}'
