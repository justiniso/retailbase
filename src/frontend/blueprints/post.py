# -*- coding: utf-8 -*-

import requests

from flask import Blueprint, request, render_template, jsonify, send_from_directory

from src.frontend.blueprints import base

bp = Blueprint(
    'post',
    __name__
)


@bp.route('/post/<int:post_id>', methods=['GET'])
def post(post_id, _request=request):

    # TODO: make this crap reusable
    response = requests.get('http://localhost:5000/api/post/{}'.format(post_id))

    if response.status_code == 404:
        return base.page_not_found()

    elif response.status_code != 200:
        return response.content

    import json
    pst = json.loads(response.content.decode('utf-8'))
    return render_template('post.html', **{'post': pst})

