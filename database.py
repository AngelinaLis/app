import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_PASSWORD, DB_USER
from models import Base
from settings import DATABASE_URL

try:
    conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = conn.cursor()
    conn.autocommit = True
    notes = "CREATE DATABASE notes"
    cursor.execute(notes)
    cursor.close()
    conn.close()
    print("The database has been created")
except:
    print("Fail")
finally:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(engine)
    Base.metadata.create_all(engine, checkfirst=True)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
