# -*- coding: utf-8 -*-
import datetime
import locale
import urlparse
import re
import urllib

from flask_restful import Resource, abort, Api, fields, marshal_with, reqparse
from mongoengine import ValidationError, queryset_manager, DoesNotExist

from . import Base
from src.api import api_app, db


class Post(Base, db.Document):

    __tablename__ = 'post'

    title = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=3000)
    brand = db.StringField(max_length=255)
    slug = db.StringField(max_length=255, required=True)
    link_url = db.StringField(max_length=2080, required=True)
    price = db.FloatField(min_value=0)
    thumbnail_url = db.StringField(max_length=2080)
    create_date = db.DateTimeField(default=datetime.datetime.now)
    publish_date = db.DateTimeField()
    delete_date = db.DateTimeField()

    tags = db.ListField(db.StringField(max_length=30))

    @queryset_manager
    def objects(cls, queryset):
        """Default order of posts by descending date"""
        return queryset.order_by('-date')

    def format_price(self):
        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
        return locale.currency(self.price) if self.price else ''

    def parse_domain(self):
        """Extract the domain (netloc) from the link url. If it cannot be parsed, return empty string"""
        domain = urlparse.urlparse(self.link_url).netloc
        domain = domain.replace('www.', '').replace('www1.', '')
        return domain

public_fields = {
    'id': fields.String,
    'title': fields.String,
    'slug': fields.String,
    'description': fields.String,
    'brand': fields.String,
    'price': fields.Float,
    'thumbnail_url': fields.String,
    'link_url': fields.String,
    'publish_date': fields.DateTime,
    'create_date': fields.DateTime,
    'delete_date': fields.DateTime,
    'tags': fields.List(fields.String),
}


def parse_tags(tagstring):
    if tagstring is None:
        return []
    tagstring = re.sub(r'(,\s+)', ',', tagstring)
    return [s.strip() for s in tagstring.split(',')]


class PostResource(Resource):

    @marshal_with(public_fields)
    def get(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except ValidationError:
            post = Post.objects.get_or_404(slug=post_id)

        if post is None:
            abort(404)

        return post

    @marshal_with(public_fields)
    def put(self, post_id):
        post = Post.objects.get_or_404(id=post_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=unicode)
        parser.add_argument('description', type=unicode)
        parser.add_argument('brand', type=unicode)
        parser.add_argument('price', type=float)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('link_url', type=str)
        parser.add_argument('publish_date', type=str)
        parser.add_argument('tags', type=str)

        data = parser.parse_args(strict=True)

        # TODO: figure out a way to handle explicitly setting a certain property to none
        for key in data.keys():
            if data[key] is None:
                data.pop(key)

        data['tags'] = parse_tags(data['tags'])
        data['brand'] = data.get('brand', post.parse_domain())
        post.update(**data)

        return post

    def delete(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except ValidationError:
            post = Post.objects.get_or_404(slug=post_id)

        post.delete()

        return {'status': 'ok'}


def validate_slug(slug):
    assert slug
    assert str(slug)
    assert slug.lower() == slug
    assert len(slug) < 50
    assert urllib.quote_plus(slug) == slug


class PostsResource(Resource):

    @marshal_with(public_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=unicode, required=True)
        parser.add_argument('description', type=unicode, required=True)
        parser.add_argument('brand', type=str)
        parser.add_argument('slug', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('link_url', type=str)
        parser.add_argument('publish_date', type=str)
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
                Post.objects.get(slug=data['slug'])
            except DoesNotExist:
                break
            else:
                count = data['slug'][-1]
                if str.isdigit(count):
                    data['slug'] = data['slug'][:-1] + str(int(count) + 1)
                else:
                    data['slug'] += '2'

        pst = Post(**data)
        pst.brand = pst.brand or pst.parse_domain()
        pst.save()

        return pst

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

        posts = Post.objects(**data).limit(limit)
        return {'results': posts}


api = Api(api_app)
api.add_resource(PostsResource, '/post')
api.add_resource(PostResource, '/post/<post_id>')