# -*- coding: utf-8 -*-

import sys

import os
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

__all__ = ['api_app']

# Add this path; note this MUST go above project imports
sys.path.append(os.path.dirname(__file__))

# Cannot import app without this:
sys.path.insert(0, os.path.dirname(__file__))

# These imports must be below all path modifications
from src.api import api_app
from src.frontend import frontend_app


application = DispatcherMiddleware(frontend_app, {'/api': api_app})

# Dev mode
if __name__ == '__main__':

    frontend_app.config['ASSETS_DEBUG'] = True

    # Activate debug mode for dev
    api_app.debug = True
    frontend_app.debug = True

    run_simple('127.0.0.1', 5000, application, use_reloader=True, use_debugger=True, threaded=False)

