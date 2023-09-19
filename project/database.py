import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

url = os.environ['POSTGRES_URL']

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
