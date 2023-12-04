#!/usr/bin/env python
# coding: utf-8
import os
import pytest

# -----------------------------------------------------------------------------
# --- Parser ---
# -----------------------------------------------------------------------------
from app.utils.file_manager import FileManager


# -----------------------------------------------------------------------------
#  ______   ______     ______     ______   ______
# /\__  _\ /\  ___\   /\  ___\   /\__  _\ /\  ___\
# \/_/\ \/ \ \  __\   \ \___  \  \/_/\ \/ \ \___  \
#    \ \_\  \ \_____\  \/\_____\    \ \_\  \/\_____\
#     \/_/   \/_____/   \/_____/     \/_/   \/_____/
#
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "param", ["doc", "name", "namespace", "type", "fields"]
)
def test_avro_schema(param: str):
    file_manager = FileManager()

    schema = file_manager.get_avro_schema()

    assert param in schema
    assert type(schema) is dict


def test_get_full_path(dir_path: str = "/file_storage/raw/sales/2022-08-09"):
    file_manager = FileManager()
    current_dir = os.getcwd()

    full_path = file_manager.get_full_path(dir_path)

    assert "".join([current_dir, dir_path]) == full_path
    assert type(full_path) is str


def test_all_folder_files(raw_dir: str = "/file_storage/raw/sales/2022-08-09"):
    file_manager = FileManager()

    folder_files = file_manager.get_all_folder_files(raw_dir)

    assert len(folder_files) > 0
    assert type(folder_files) is list


def test_read_file(
        dir_path: str = "/file_storage/raw/sales/2022-08-09",
        file_name: str = "sales_2022-08-09.json"):
    file_manager = FileManager()
    full_path = file_manager.get_full_path(dir_path)
    file_path = "/".join([full_path, file_name])

    file_data = file_manager.read_file(file_path)

    assert len(file_data) > 0
    assert type(file_data) is list


def test_save_raw_data(
        date: str = "2022-08-09",
        raw_dir: str = "/file_storage/raw/sales/2022-08-09"):
    file_name: str = "sales_2022-08-09.json"
    client_dict = {
        "client": "Michael Wilkerson",
        "purchase_date": "2022-08-10",
        "product": "Vacuum cleaner",
        "price": 346
    }
    file_manager = FileManager()
    folder_files = [
        str(f).rsplit('/', maxsplit=1)[-1]
        for f in file_manager.get_all_folder_files(raw_dir)
    ]

    file_manager.save_raw_data([client_dict], date, raw_dir)

    assert file_name in folder_files


def test_convert_raw_data(
        raw_dir: str = "/file_storage/raw/sales/2022-08-09",
        stg_dir: str = "/file_storage/stg/sales/2022-08-09"):
    file_manager = FileManager()
    folder_list = file_manager.get_all_folder_files(raw_dir)

    file_manager.convert_raw_data(raw_dir, stg_dir)
    folder_stg_list = file_manager.get_all_folder_files(stg_dir)

    assert len(folder_list) == len(folder_stg_list)
