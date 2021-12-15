from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3306/sgtdevsaser")
Session = sessionmaker(bind=engine)

Base = declarative_base()