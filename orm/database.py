import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm.models import Base

load_dotenv()
DATABASE_HOST=os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT=os.getenv('DATABASE_PORT', '5432')
DATABASE_PASS=os.getenv('DATABASE_PASS', 'postgres')
DATABASE_USER=os.getenv('DATABASE_USER', 'postgres')
DATABASE_NAME=os.getenv('DATABASE_NAME', 'postgres')

DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
engine = create_engine(DATABASE_URL) # Connect to database
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)