import glob
import os
from pathlib import Path


def rename_newest_file(new_file: Path):
    '''Rename the newest (last-modified) file from the folder of new_file
    with the name of new_file'''
    folder = new_file.parent
    extension = f'*{new_file.suffix}'
    list_of_files = glob.glob(str(folder / extension))
    newest_file = max(list_of_files, key=os.path.getctime)
    return Path(newest_file).rename(new_file)
