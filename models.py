import datetime

from peewee import Model, TextField, DateTimeField, DateField, IntegerField

from app import db

class Link(Model):
    short_code = TextField(primary_key=True)
    original_url = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = "links"


class DailyStats(Model):
    short_code = TextField()
    report_date = DateField(default=datetime.date.today)
    hits = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        indexes = (
            (('short_code', 'report_date'), True),
        )
        primary_key = False
        table_name = "daily_stats"
