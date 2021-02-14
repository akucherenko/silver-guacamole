from os import environ

from flask import Flask
from peewee import PostgresqlDatabase

APP_HOST = environ["APP_HOST"]

app = Flask(__name__)
app.config.from_object(__name__)
db = PostgresqlDatabase(environ["DB_NAME"],
                        user=environ["DB_USER"],
                        password=environ["DB_PASSWORD"],
                        host=environ["DB_HOST"],
                        port=environ["DB_PORT"])
