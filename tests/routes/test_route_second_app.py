#!/usr/bin/env python
# coding: utf-8
import pytest

# -----------------------------------------------------------------------------
# --- HTTP status ---
# -----------------------------------------------------------------------------
from http import HTTPStatus

# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import Flask


# -----------------------------------------------------------------------------
#  ______   ______     ______     ______   ______
# /\__  _\ /\  ___\   /\  ___\   /\__  _\ /\  ___\
# \/_/\ \/ \ \  __\   \ \___  \  \/_/\ \/ \ \___  \
#    \ \_\  \ \_____\  \/\_____\    \ \_\  \/\_____\
#     \/_/   \/_____/   \/_____/     \/_/   \/_____/
#
# -----------------------------------------------------------------------------
def test_empty_raw_dir_param(second_flask_app: Flask):
    with second_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "raw_dir": "",
            "stg_dir": "/file_storage/stg/sales/2022-08-09"
        })

        assert response.status_code == HTTPStatus.BAD_REQUEST


def test_empty_stg_dir_param(second_flask_app: Flask):
    with second_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "raw_dir": "/file_storage/raw/sales/2022-08-09",
            "stg_dir": ""
        })

        assert response.status_code == HTTPStatus.BAD_REQUEST


def test_wrong_params_type(second_flask_app: Flask):
    with second_flask_app.test_client() as test_client:
        response = test_client.post('/', data={
            "raw_dir": "/file_storage/raw/sales/2022-08-09",
            "stg_dir": "/file_storage/stg/sales/2022-08-09"
        })

        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


@pytest.mark.parametrize("date", ["2022-08-09", "2022-08-10", "2022-08-11"])
def test_main_url(second_flask_app: Flask, date: str):
    with second_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "raw_dir": f"/file_storage/raw/sales/{date}",
            "stg_dir": f"/file_storage/stg/sales/{date}"
        })

        assert response.status_code == HTTPStatus.CREATED
