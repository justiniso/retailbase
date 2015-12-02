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
    featured_category_slugs = ['gifts-for-him', 'gadget-gifts']
    categories = Category.objects(slug__in=featured_category_slugs)

    all_tags = Post.objects.distinct('tags')
    return render_template('home.html', categories=categories, all_tags=all_tags)