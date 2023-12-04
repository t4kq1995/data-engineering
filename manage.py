#!/usr/bin/env python
# coding: utf-8
import sys

# -----------------------------------------------------------------------------
# --- App settings ---
# -----------------------------------------------------------------------------
from app.app import create_first_app, create_second_app

# -----------------------------------------------------------------------------
# --- Config---
# -----------------------------------------------------------------------------
from config import ConfigPath

# -----------------------------------------------------------------------------
# --- Mode detector ---
# -----------------------------------------------------------------------------
application_mode = str(sys.argv[1])

# -----------------------------------------------------------------------------
match application_mode:
    case "first_app":
        app = create_first_app(config_path=ConfigPath.development)
        app.run(
            use_debugger=app.config["DEBUG"],
            use_reloader=True,
            host=app.config["IP_ADDRESS"],
            port=app.config["FIRST_API_PORT"]
        )

    case "second_app":
        app = create_second_app(config_path=ConfigPath.development)
        app.run(
            use_debugger=app.config["DEBUG"],
            use_reloader=True,
            host=app.config["IP_ADDRESS"],
            port=app.config["SECOND_API_PORT"]
        )

    case _:
        pass
