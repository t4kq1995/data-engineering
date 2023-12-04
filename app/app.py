#!/usr/bin/env python
# coding: utf-8
# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import Flask
from flask_restful import Api

# -----------------------------------------------------------------------------
# --- Config ---
# -----------------------------------------------------------------------------
from config import Config


def create_first_app(config_path: str = "conf/development.conf") -> Flask:
    app = Flask(__name__)
    # -------------------------------------------------------------------------
    # --- Init config ---
    # -------------------------------------------------------------------------
    config = Config(app, config_path)
    config.setup_environment()

    # -------------------------------------------------------------------------
    # --- Register blueprints for routing ---
    # -------------------------------------------------------------------------
    from app.api.routes.first_app import first_app_bp, Main
    api = Api(first_app_bp)
    app.register_blueprint(first_app_bp)

    # -------------------------------------------------------------------------
    # --- Routing ---
    # -------------------------------------------------------------------------
    api.add_resource(Main, '/')

    return app


def create_second_app(config_path: str = "conf/development.conf") -> Flask:
    app = Flask(__name__)
    # -------------------------------------------------------------------------
    # --- Init config ---
    # -------------------------------------------------------------------------
    config = Config(app, config_path)
    config.setup_environment()

    # -------------------------------------------------------------------------
    # --- Register blueprints for routing ---
    # -------------------------------------------------------------------------
    from app.api.routes.second_app import second_app_bp, Main
    api = Api(second_app_bp)
    app.register_blueprint(second_app_bp)

    # -------------------------------------------------------------------------
    # --- Routing ---
    # -------------------------------------------------------------------------
    api.add_resource(Main, '/')

    return app
