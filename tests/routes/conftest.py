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
from app.app import create_second_app


@pytest.fixture(scope="session")
def second_flask_app() -> Flask:
    return create_second_app(config_path=ConfigPath.development)
