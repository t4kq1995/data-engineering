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
from app.utils.parser import Parser
from app.utils.file_manager import FileManager

# -----------------------------------------------------------------------------
# --- blueprint ---
# -----------------------------------------------------------------------------
first_app_bp = Blueprint(name='first_app_api', import_name=__name__)


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
            'date', type=str, required=True, help="date cannot be blank"
        )
        parser.add_argument(
            'raw_dir', type=str, required=True, help="raw_dir cannot be blank"
        )
        args = parser.parse_args()

        # ---------------------------------------------------------------------
        # --- Validator ---
        # ---------------------------------------------------------------------
        if args["date"] == "" or args["raw_dir"] == "":
            return {
                "success": False,
                "message": "Please provide valid data"
            }, 400

        # ---------------------------------------------------------------------
        # --- Logging ---
        # ---------------------------------------------------------------------
        logger.debug(f"/first_app --> {args['date']} --> {args['raw_dir']}")

        # ---------------------------------------------------------------------
        # --- Parse data and save ---
        # ---------------------------------------------------------------------
        parser = Parser()
        date_data = parser.collect_sales_data(args["date"])

        # ---------------------------------------------------------------------
        file_manager = FileManager()
        file_manager.save_raw_data(date_data, args["date"], args["raw_dir"])

        return {
            "success": True,
            "message": "Data retrieved successfully from API"
        }, 201
