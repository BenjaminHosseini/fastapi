# using ORM to talk to databse. instead of writing SQL code queries we
# can write standard python codes. ORM converts it to SQL code 
# SQLALCHEMY is a popular python ORM -> pip install sqlalchemy
# sqlalchemy needs a databse driver -> psycopg for postgres

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg   # database connection
from psycopg.rows import dict_row
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine is responsible for establishing the connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#-------Database connection using SQL not sqlAlchemy(we don't below code if use sqlalchemy) ----------
# database connection with psycopg -> pip install psycopg
#  -> i had to used this version -> pip install psycopg\[binary\]
# import psycopg
while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi',
                            user='postgres', password='9986', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connectiong to database failed")
        print("Error: ", error)
        time.sleep(2)