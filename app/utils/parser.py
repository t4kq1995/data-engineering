#!/usr/bin/env python
# coding: utf-8
# -----------------------------------------------------------------------------
# --- Typing ---
# -----------------------------------------------------------------------------
from typing import List

# -----------------------------------------------------------------------------
# --- Requests ---
# -----------------------------------------------------------------------------
import requests

# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import current_app


class Parser:
    def __init__(self):
        self.url = current_app.config.get("API_URL", "")
        self.auth_token = current_app.config.get("AUTH_TOKEN", "")

    def make_request(self, date: str, page: int) -> List:
        response = requests.get(
            url=self.url, params={"date": date, "page": page},
            headers={'Authorization': self.auth_token}, timeout=(2, 5)
        )

        if response.status_code == 200:
            return response.json()
        return []

    def collect_sales_data(self, date: str, max_pages: int = 100) -> List:
        date_data = []
        for page in range(1, max_pages):
            data = self.make_request(date, page)
            if not data:
                break
            date_data.extend(data)
        return date_data
