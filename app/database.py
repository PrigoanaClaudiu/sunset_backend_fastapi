import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_pass}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# cursor_factory? = gives you the columns and what are on these columns
#while  True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fatapi', 
#                                user='postgres', password='qwe', cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("ii bun")
#        break
#    except Exception as e:
#        print("Connecting to database failled")
#        print("Error:", e)
#        time.sleep(3)

