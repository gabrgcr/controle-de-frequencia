from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:z9cr7NBvKwHZIqW3@db.wcxbroydbesbruzopdzr.supabase.co:6543/postgres")
Session = sessionmaker(bind=engine)
session = Session()
