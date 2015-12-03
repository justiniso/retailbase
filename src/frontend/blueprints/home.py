# -*- coding: utf-8 -*-
from collections import OrderedDict

from flask import Blueprint, request, render_template
from src.api.model.category import Category
from src.api.model.post import Post


bp = Blueprint(
    'home',
    __name__
)

@bp.route('/', methods=['GET'])
def home(_request=request):
    all_tags = Post.objects.distinct('tags')
    return render_template('home.html', all_tags=all_tags)