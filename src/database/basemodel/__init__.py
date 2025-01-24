import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from src.utils import db_user, db_name, db_pass, db_port, db_host
Base = declarative_base()
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@host:{db_port}/{db_name}"

pool = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name,
    )
    , echo=True
)
print(sqlalchemy.engine.url.URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name,
    ))