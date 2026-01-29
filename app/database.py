from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# FIXED URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres',
#                              password= '', cursor_factory= RealDictCursor)
#     cursor = conn.cursor()
#     print("Database Connection was successful")
# except Exception as error:
#     print("Connection to dtabase failed")
#     print("Error:", error)

# my_posts = [{"title": "post 1", "content": "content of post 1", "id": 1},
#             {"title": "post 2", "content": "content of post 2", "id": 2}]