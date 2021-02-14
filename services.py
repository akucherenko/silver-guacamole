import random
import string

from peewee import DoesNotExist
from psycopg2 import errors as db_err

from app import db
from models import Link, DailyStats


def _random_code(length):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


class ShortCodeGenerationFailure(BaseException):
    pass


class Shortener:
    CODE_LENGTH = 5
    NUM_TEMP_CODES = 10
    MAX_ATTEMPTS = 5

    def __init__(self, gen=_random_code):
        self._generate = gen

    def save_url(self, url):
        uniq_attempt = self.MAX_ATTEMPTS

        while uniq_attempt > 0:
            codes = [self._generate(self.CODE_LENGTH) for _ in range(self.NUM_TEMP_CODES)]
            existing = [l.short_code for l in Link.select(Link.short_code).where(Link.short_code.in_(codes))]
            codes = [c for c in codes if c not in existing]
            try:
                Link.insert(short_code=codes[0], original_url=url).execute()
                return codes[0]
            except db_err.UniqueViolation:
                db.rollback()
                uniq_attempt -= 1
            except db_err.DatabaseError as err:
                db.rollback()
                raise RuntimeError("Error saving a link record.", exc_info=err)

        raise ShortCodeGenerationFailure


class Resolver:

    def retrieve_link(self, short_code):
        link = None
        try:
            link = Link.get(Link.short_code == short_code)
        except DoesNotExist:
            pass
        return link


class LinkStatistics:

    def increment(self, link, date_):
        DailyStats.insert(short_code=link.short_code, report_date=date_, hits=1).on_conflict(
            conflict_target=[DailyStats.short_code, DailyStats.report_date],
            preserve=[],
            update={DailyStats.hits: DailyStats.hits + 1}
        ).execute()
