# -*- coding: utf-8 -*-

import requests

from flask import Blueprint, request, render_template, jsonify, send_from_directory
from src.api.model.post import Post

from src.frontend.blueprints import base

bp = Blueprint(
    'post',
    __name__
)


@bp.route('/gift/<slug>', methods=['GET'])
def post(slug, _request=request):

    try:
        pst = Post.objects(slug=slug)[0]
    except IndexError:
        return base.page_not_found()

    return render_template('post.html', post=pst)

