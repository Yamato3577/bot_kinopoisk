from peewee import *
from pathlib import Path

from datetime import datetime


db = SqliteDatabase(Path('database', 'data.db'))


class BaseModel(Model):
    class Meta:
        database = db

    created_data = DateField(default=datetime.now())


class Favourite(BaseModel):
    class Meta:
        db_table = 'Favourites'

    id_user = IntegerField()
    nickname = CharField()
    id_movie = IntegerField(null=True)
    name = CharField(null=True)
    type_movie = CharField(null=True)
    countries = CharField(null=True)
    rating = FloatField(null=True)
    description = CharField(null=True)
    year = IntegerField(null=True)
    poster = CharField(null=True)
    genres = CharField(null=True)
    trailer = CharField(null=True)


db.create_tables([Favourite])
