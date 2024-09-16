from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_username = "postgres"
db_pass = "admin"

db_port = "5433"
db_host = "localhost"

db_name = "Quiz_Application"

conn_string = f"postgresql://{db_username}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(conn_string)

Session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
