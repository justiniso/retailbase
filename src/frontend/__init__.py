# -*- coding: utf-8 -*-

import os

from . import blueprints
from src import appfactory


def create_frontend_app():
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'static')

    app = appfactory.create_app(
        'frontend',
        blueprints=blueprints,
        static_folder=static_folder,
        template_folder=template_folder)

    return app


frontend_app = create_frontend_app()
