#!/usr/bin/env python
# coding: utf-8
# -----------------------------------------------------------------------------
# --- Logger ---
# -----------------------------------------------------------------------------
from loguru import logger

# -----------------------------------------------------------------------------
# --- Flask ---
# -----------------------------------------------------------------------------
from flask import Blueprint, typing
from flask_restful import Resource, reqparse

# -----------------------------------------------------------------------------
# --- Utils ---
# -----------------------------------------------------------------------------
from app.utils.file_manager import FileManager

# -----------------------------------------------------------------------------
# --- blueprint ---
# -----------------------------------------------------------------------------
second_app_bp = Blueprint(name='second_app_api', import_name=__name__)


# --------------------------------------------------------------------------- #
#
#  ______     __  __     ______   __  __
# /\  __ \   /\ \/\ \   /\__  _\ /\ \_\ \
# \ \  __ \  \ \ \_\ \  \/_/\ \/ \ \  __ \
#  \ \_\ \_\  \ \_____\    \ \_\  \ \_\ \_\
#   \/_/\/_/   \/_____/     \/_/   \/_/\/_/
#
#
# --------------------------------------------------------------------------- #
class Main(Resource):
    @staticmethod
    def post() -> typing.ResponseReturnValue:
        # ---------------------------------------------------------------------
        # --- Parse params ---
        # ---------------------------------------------------------------------
        parser = reqparse.RequestParser()
        parser.add_argument(
            'stg_dir', type=str, required=True, help="stg_dir cannot be blank"
        )
        parser.add_argument(
            'raw_dir', type=str, required=True, help="raw_dir cannot be blank"
        )
        args = parser.parse_args()

        # ---------------------------------------------------------------------
        # --- Validator ---
        # ---------------------------------------------------------------------
        if args["stg_dir"] == "" or args["raw_dir"] == "":
            return {
                "success": False,
                "message": "Please provide valid data"
            }, 400

        # ---------------------------------------------------------------------
        # --- Logging ---
        # ---------------------------------------------------------------------
        logger.debug(f"/sec_app --> {args['stg_dir']} --> {args['raw_dir']}")

        # ---------------------------------------------------------------------
        # --- Convert data ---
        # ---------------------------------------------------------------------
        file_manager = FileManager()
        file_manager.convert_raw_data(args['raw_dir'], args['stg_dir'])

        return {
            "success": True,
            "message": "Data converted successfully from raw file"
        }, 201
