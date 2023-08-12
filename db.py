from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///database/productos.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()