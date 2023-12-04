#!/usr/bin/env python
# coding: utf-8
import configparser

# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import Flask

# -----------------------------------------------------------------------------
# --- Typing ---
# -----------------------------------------------------------------------------
from typing import NoReturn


class ConfigPath:
    development = "conf/development.conf"


class Config:
    def __init__(self, app: Flask, config_path: str):
        # ---------------------------------------------------------------------
        self.app = app
        self.config_path = config_path

    def setup_environment(self, section: str = "config") -> NoReturn:
        # ---------------------------------------------------------------------
        # --- Read params from config file ---
        # ---------------------------------------------------------------------
        config = configparser.ConfigParser()
        config.read(self.config_path)
        for key, value in config[section].items():
            self.app.config[key.upper()] = value
