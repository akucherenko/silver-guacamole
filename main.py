from app import app, db
from models import Link, DailyStats
import handlers

if __name__ == '__main__':
    db.create_tables([Link, DailyStats])
    app.run(host="0.0.0.0")
