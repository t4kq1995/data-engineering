#!/usr/bin/env python
# coding: utf-8
import pytest

# -----------------------------------------------------------------------------
# --- Config---
# -----------------------------------------------------------------------------
from config import ConfigPath

# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import Flask

# -----------------------------------------------------------------------------
# --- Modules ---
# -----------------------------------------------------------------------------
from app.app import create_first_app


@pytest.fixture(scope="session")
def first_flask_app() -> Flask:
    return create_first_app(config_path=ConfigPath.development)
