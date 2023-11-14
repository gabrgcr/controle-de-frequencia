import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = os.environ['POSTGRES_URL']

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
