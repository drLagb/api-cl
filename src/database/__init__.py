import sqlalchemy
from src.utils import db_user, db_name, db_pass, db_port, db_host
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