# -*- coding: utf-8 -*-

import uuid
import datetime

import dateutil.parser

from src.api import db


# http://prschmid.blogspot.com/2012/12/json-serializing-sqlalchemy-objects.html
class JsonSerializer(object):
    """A serializer that provides methods to serialize and deserialize JSON
    dictionaries.

    Note, one of the assumptions this serializer makes is that all objects that
    it is used to deserialize have a constructor that can take all of the
    attribute arguments. I.e. If you have an object with 3 attributes, the
    constructor needs to take those three attributes as keyword arguments.
    """

    __attributes__ = None
    """The attributes to be serialized by the serializer.
    The implementer needs to provide these."""

    __required__ = None
    """The attributes that are required when deserializing.
    The implementer needs to provide these."""

    __attribute_serializer__ = None
    """The serializer to use for a specified attribute. If an attribute is not
    included here, no special serializer will be user.
    The implementer needs to provide these."""

    serializers = {
        'id': {
            'serialize': lambda x: uuid.UUID(bytes=x).hex,
            'deserialize': lambda x: uuid.UUID(hex=x).bytes
        },
        'date': {
            'serialize': lambda x, tz: x.isoformat(),
            'deserialize': lambda x: dateutil.parser.parse(x)
        }
    }

    def deserialize(self):
        """TODO: Needs to be implemented"""
        raise NotImplementedError

    def serialize(self):
        """Serialize instance to a dictionary.

        Take all of the attributes defined in self.__attributes__ and create
        a dictionary containing those values.
        """
        d = dict()
        for attr in self.__attributes__:
            val = getattr(self, attr)
            if val is None:
                continue
            serializer = self.__attribute_serializer__.get(attr)
            if serializer:
                d[attr] = self.serializers[serializer]['serialize'](val)
            else:
                d[attr] = val

        return d


class BaseModel(JsonSerializer):

    @property
    def __tablename__(cls):
        return cls.__name__.lower()


Base = BaseModel
