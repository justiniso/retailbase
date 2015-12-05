# -*- coding: utf-8 -*-
import datetime
import re
import urllib

from flask_restful import Resource, abort, Api, fields, marshal_with, reqparse
from mongoengine import ValidationError, queryset_manager, DoesNotExist

from . import Base
from src.api import api_app, db


class Category(Base, db.Document):

    title = db.StringField(max_length=255, required=True)
    caption = db.StringField(max_length=255)
    body = db.StringField()
    slug = db.StringField(max_length=255, required=True)
    thumbnail_url = db.StringField(max_length=2080)
    banner_url = db.StringField(max_length=2080)
    create_date = db.DateTimeField(default=datetime.datetime.now)
    tags = db.ListField(db.StringField(max_length=30))

    @queryset_manager
    def objects(cls, queryset):
        """Default order of posts by descending date"""
        return queryset.order_by('-title')


public_fields = {
    'id': fields.String,
    'title': fields.String,
    'caption': fields.String,
    'body': fields.String,
    'slug': fields.String,
    'thumbnail_url': fields.String,
    'banner_url': fields.String,
    'create_date': fields.DateTime,
    'tags': fields.List(fields.String)
}


def parse_tags(tagstring):
    if tagstring is None:
        return []
    tagstring = re.sub(r'(,\s+)', ',', tagstring)
    return [s.strip() for s in tagstring.split(',')]


class CategoryResource(Resource):

    @marshal_with(public_fields)
    def get(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except ValidationError:
            category = Category.objects.get_or_404(slug=category_id)

        if category is None:
            abort(404)

        return category

    @marshal_with(public_fields)
    def put(self, category_id):
        category = Category.objects.get_or_404(id=category_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=unicode)
        parser.add_argument('caption', type=unicode)
        parser.add_argument('body', type=unicode)
        parser.add_argument('slug', type=str)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('banner_url', type=str)
        parser.add_argument('tags', type=str)

        data = parser.parse_args(strict=True)

        # TODO: figure out a way to handle explicitly setting a certain property to none
        for key in data.keys():
            if data[key] is None:
                data.pop(key)

        if data.get('tags'):
            data['tags'] = parse_tags(data['tags'])
        category.update(**data)

        return category

    def delete(self, post_id):
        try:
            category = Category.objects.get(id=post_id)
        except ValidationError:
            category = Category.objects.get_or_404(slug=post_id)

        category.delete()

        return {'status': 'ok'}


def validate_slug(slug):
    assert slug
    assert str(slug)
    assert slug.lower() == slug
    assert len(slug) < 80
    assert urllib.quote_plus(slug) == slug


class CategoriesResource(Resource):

    @marshal_with(public_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=unicode, required=True)
        parser.add_argument('caption', type=unicode)
        parser.add_argument('body', type=unicode)
        parser.add_argument('slug', type=str)
        parser.add_argument('banner_url', type=str)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('banner_url', type=str)
        parser.add_argument('tags', type=unicode)

        data = parser.parse_args(strict=True)
        validate_slug(data['slug'])
        data['tags'] = parse_tags(data['tags'])

        # Find a unique slug
        # Try to find an object with the slug; if none exist, use it. Otherwise
        # continue to iterate over integers until we find one that does not exist
        # TODO: make reusable and testable
        while True:
            try:
                Category.objects.get(slug=data['slug'])
            except DoesNotExist:
                break
            else:
                count = data['slug'][-1]
                if str.isdigit(count):
                    data['slug'] = data['slug'][:-1] + str(int(count) + 1)
                else:
                    data['slug'] += '2'

        cat = Category(**data)
        cat.save()

        return cat

    @marshal_with({'results': fields.List(fields.Nested(public_fields))})
    def get(self, limit=100):
        """
        Query endpoint

        Prepend fields with "$regex:" if the search should be a regex
        search on that field. Search terms will be joined by "and"
        not "or"
        """
        regex_flag = '$regex:'

        parser = reqparse.RequestParser()
        parser.add_argument('tags', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('slug', type=str)
        data = parser.parse_args()

        # TODO: abstract this please
        for key in data.keys():
            if data[key] is None:
                data.pop(key)
            elif isinstance(data[key], basestring) and data[key].startswith(regex_flag):
                data[key] = {'$regex': data[key].replace(regex_flag, '')}

        cats = Category.objects(**data).limit(limit)
        return {'results': cats}


api = Api(api_app)
api.add_resource(CategoriesResource, '/category')
api.add_resource(CategoryResource, '/category/<category_id>')