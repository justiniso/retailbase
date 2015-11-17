# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify, send_from_directory


bp = Blueprint(
    'base',
    __name__
)

@bp.route('/healthcheck')
def healthcheck(_request=request):
    return jsonify(result={'status': 'ok'})


@bp.route('/styleguide')
def styleguide(_request=request):
    return render_template('styleguide.html')

@bp.route('/robots.txt')
def robots(_request=request):
    import os
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(template_dir, 'robots.txt')

@bp.errorhandler(404)
def page_not_found(*args, **kwargs):
    return render_template('404.html'), 404

