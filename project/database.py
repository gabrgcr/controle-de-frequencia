from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("mysql+pymysql://admin:admin@localhost:3306/controle_de_frequencia_db?")
Session = sessionmaker(bind=engine)
session = Session()
