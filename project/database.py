import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

url = os.environ['DATABASE_URL']

engine = create_engine("postgresql://" + url)
Session = sessionmaker(bind=engine)
session = Session()
