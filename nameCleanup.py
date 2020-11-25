import sys
from pathlib import Path
import os
import re


def remove_year(folder_name):
    movie_year_regex = re.compile(r'^(.*)(\d{4})*.(\d{4})(.*)$')
    year = movie_year_regex.search(folder_name)

    new_folder_name = year.group(1)
    if year.group(2) is not None:
        new_folder_name = new_folder_name + year.group(2)
    if year.group(4) is not None:
        new_folder_name = new_folder_name + year.group(4)
    return new_folder_name


def remove_joining_periods(name_to_edit):
    period_regex = re.compile(r'(\w)(\.)(\w)')
    periods = period_regex.search(name_to_edit)
    if periods:
        return period_regex.sub(r'\1 \3', name_to_edit)
    else:
        return name_to_edit


def remove_trailing_period(name_to_edit):
    period_regex = re.compile(r'(\w|\d)(\.)$')
    periods = period_regex.search(name_to_edit)
    if periods:
        return period_regex.sub(r'\1', name_to_edit)
    else:
        return name_to_edit


def rename_folder(dir_path, old_name, new_name):
    new_folder_path = dir_path / Path(new_name)
    old_folder_path = dir_path / Path(old_name)
    os.rename(old_folder_path, new_folder_path)


def clean_folder_names(dir_path, folders):
    for folder in folders:
        if '1080p' in folder:
            name_to_edit = folder.split('1080p')
            name_to_edit = name_to_edit[0]
            str(Path(dir_path) / folder)
        elif '2160p' in folder:
            name_to_edit = folder.split('1080p')
            name_to_edit = name_to_edit[0]
        else:
            continue

        if ' ' in folder:
            continue

        name_to_edit = remove_year(name_to_edit)
        name_to_edit = remove_joining_periods(name_to_edit)
        new_name = remove_trailing_period(name_to_edit)
        rename_folder(dir_path, folder, new_name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python nameCleanup.py [folder path to clean]')
        sys.exit()

    folder_path = sys.argv[1]
    locationToClean = Path(folder_path)
    if locationToClean.exists():
        filesInFolder = os.listdir(locationToClean)
        clean_folder_names(locationToClean, filesInFolder)
    else:
        print('non-existent path, please re-run with valid path')
        sys.exit()