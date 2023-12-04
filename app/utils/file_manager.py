#!/usr/bin/env python
# coding: utf-8
import os
import json

# -----------------------------------------------------------------------------
# --- Path ---
# -----------------------------------------------------------------------------
from pathlib import Path

# -----------------------------------------------------------------------------
# --- Typing ---
# -----------------------------------------------------------------------------
from typing import List, NoReturn, Dict

# -----------------------------------------------------------------------------
# --- Avro ---
# -----------------------------------------------------------------------------
from fastavro import writer, parse_schema


class FileManager:
    @staticmethod
    def get_avro_schema() -> Dict:
        return {
            'doc': 'A sales reading.',
            'name': 'Sales',
            'namespace': 'development',
            'type': 'record',
            'fields': [
                {'name': 'client', 'type': 'string'},
                {'name': 'purchase_date', 'type': 'string'},
                {'name': 'product', 'type': 'string'},
                {'name': 'price', 'type': 'int'}
            ]
        }

    @staticmethod
    def get_full_path(dir_path: str) -> str:
        return "".join([os.getcwd(), dir_path])

    @staticmethod
    def read_file(file_path: str) -> List:
        with open(file_path, encoding="utf-8") as f_read:
            file_data = json.loads(f_read.read())
        return file_data

    def get_all_folder_files(self, raw_dir: str) -> List:
        file_list = []
        full_path = self.get_full_path(raw_dir)
        for filepath in Path(full_path).glob('**/*'):
            file_list.append(filepath.absolute())
        return file_list

    def save_raw_data(self, data: List, date: str, raw_dir: str) -> NoReturn:
        file_name = f"sales_{date}.json"
        dir_path = self.get_full_path(raw_dir)
        file_path = "/".join([dir_path, file_name])

        # ---------------------------------------------------------------------
        # --- Create path if doesn't exists ---
        # ---------------------------------------------------------------------
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------------------
        # --- Write file ---
        # ---------------------------------------------------------------------
        with open(file_path, "w", encoding="utf-8") as f_write:
            f_write.write(json.dumps(data, indent=4))

    def convert_raw_data(self, raw_dir: str, stg_dir: str) -> NoReturn:
        raw_files = self.get_all_folder_files(raw_dir)
        for r_file in raw_files:
            file_data = self.read_file(r_file)

            # -----------------------------------------------------------------
            # --- Create avro schema ---
            # -----------------------------------------------------------------
            schema = self.get_avro_schema()
            parsed_schema = parse_schema(schema)

            # -----------------------------------------------------------------
            # --- Create file path ---
            # -----------------------------------------------------------------
            file_name = str(r_file).rsplit('/', maxsplit=1)[-1].replace(
                "json", "avro"
            )
            dir_path = self.get_full_path(stg_dir)
            file_path = "/".join([dir_path, file_name])

            # -----------------------------------------------------------------
            # --- Create path if doesn't exists ---
            # -----------------------------------------------------------------
            Path(dir_path).mkdir(parents=True, exist_ok=True)

            # -----------------------------------------------------------------
            # --- Write Avro file ---
            # -----------------------------------------------------------------
            with open(file_path, 'wb') as out:
                writer(out, parsed_schema, file_data)
