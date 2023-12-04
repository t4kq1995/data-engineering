#!/usr/bin/env python
# coding: utf-8
import pytest

# -----------------------------------------------------------------------------
# --- Parser ---
# -----------------------------------------------------------------------------
from app.utils.parser import Parser

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
@pytest.mark.parametrize("date", ["2022-08-09", "2022-08-10", "2022-08-11"])
@pytest.mark.parametrize("page", [1, 2, 3])
def test_good_parser_request(first_flask_app: Flask, date: str, page: int):
    with first_flask_app.app_context():
        parser = Parser()

        response = parser.make_request(date, page)

        assert len(response) > 0
        assert type(response) is list


@pytest.mark.parametrize("date", ["2022-08-09", "2022-08-10", "2022-08-11"])
@pytest.mark.parametrize("page", [100, 200, 300])
def test_bad_page_param_request(first_flask_app: Flask, date: str, page: int):
    with first_flask_app.app_context():
        parser = Parser()

        response = parser.make_request(date, page)

        assert len(response) == 0
        assert type(response) is list


@pytest.mark.parametrize("date", ["2022-08-32", "2022-08-33", "2022-08-34"])
@pytest.mark.parametrize("page", [1, 2, 3])
def test_bad_date_param_request(first_flask_app: Flask, date: str, page: int):
    with first_flask_app.app_context():
        parser = Parser()

        response = parser.make_request(date, page)

        assert len(response) == 0
        assert type(response) is list


@pytest.mark.parametrize("date", ["2022-08-09", "2022-08-10", "2022-08-11"])
def test_bad_sales_collect_data(first_flask_app: Flask, date: str):
    with first_flask_app.app_context():
        parser = Parser()

        response = parser.collect_sales_data(date)

        assert len(response) > 0
        assert type(response) is list
