#!/usr/bin/env python
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""

from collections import Container
from datetime import datetime

import pytz
from sqlalchemy.orm import joinedload

from atlas.extensions import db


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save(commit=commit) or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    @classmethod
    def get_by_field(cls, field, value):
        col = getattr(cls, field)
        return cls.query.filter(col == value).first()


class TimestampedModel(Model):
    """Mixin that add convenience methods for CRUD that also timestamps
    creation and modification times.
    """
    __abstract__ = True
    created_at = db.Column(db.DateTime(timezone=True))
    last_updated = db.Column(db.DateTime(timezone=True))

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        now = datetime.now(pytz.utc)
        self.created_at = now
        self.last_updated = now

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        now = datetime.now(pytz.utc)
        instance.created_at = now
        instance.last_updated = now
        return instance.save(commit=commit)

    def update(self, commit=True, update_timestamp=True, **kwargs):
        """Update specific fields of a record."""
        if update_timestamp:
            now = datetime.now(pytz.utc)
            self.last_updated = now
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return self.save(commit=commit, update_timestamp=update_timestamp)

    def save(self, commit=True, update_timestamp=True):
        if update_timestamp:
            now = datetime.now(pytz.utc)
            self.last_updated = now
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id, with_=[]):
        if any(
            (isinstance(id, str) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            query = cls.query

            for prop in with_:
                query = query.options(joinedload(prop))

            return query.get(int(id))
        return None

    @classmethod
    def get_by_ids(cls, ids):
        if isinstance(ids, Container) and not isinstance(ids, str):
            return cls.query.filter(cls.id.in_(ids))
        return None

    def __repr__(self):  # pragma: no cover
        return '<%s(%s)>' % (self.__class__.__name__, self.id)
