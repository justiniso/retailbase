# -*- coding: utf-8 -*-

import os

from webassets import Bundle
from flask.ext.assets import Environment

from . import blueprints
from src import appfactory


def create_frontend_app():
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets')

    # css_bundle = Bundle(
    #     'build/css/*.css',
    #     output='../../static/main.css')
    #
    # js_bundle = Bundle(
    #     'build/js/*.js',
    #     output='../../static/main.js')
    #
    # fonts_bundle = Bundle(
    #     'fonts/bootstrap/*')

    app = appfactory.create_app(
        'frontend',
        blueprints=blueprints,
        static_folder=static_folder,
        template_folder=template_folder)

    # env = Environment(app)
    # env.register('css_main', css_bundle)
    # env.register('js_main', js_bundle)
    # env.register('fonts_bundle', fonts_bundle)

    return app


frontend_app = create_frontend_app()
