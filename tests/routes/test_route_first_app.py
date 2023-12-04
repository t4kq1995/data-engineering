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
def test_empty_date_param(first_flask_app: Flask):
    with first_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "date": "",
            "raw_dir": "/file_storage/raw/sales/2022-08-09"
        })

        assert response.status_code == HTTPStatus.BAD_REQUEST


def test_empty_raw_dir_param(first_flask_app: Flask):
    with first_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "date": "2022-08-09",
            "raw_dir": ""
        })

        assert response.status_code == HTTPStatus.BAD_REQUEST


def test_wrong_params_type(first_flask_app: Flask):
    with first_flask_app.test_client() as test_client:
        response = test_client.post('/', data={
            "date": "2022-08-09",
            "raw_dir": "/file_storage/raw/sales/2022-08-09"
        })

        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


@pytest.mark.parametrize("date", ["2022-08-09", "2022-08-10", "2022-08-11"])
def test_main_url(first_flask_app: Flask, date: str):
    with first_flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "date": date,
            "raw_dir": f"/file_storage/raw/sales/{date}"
        })

        assert response.status_code == HTTPStatus.CREATED
