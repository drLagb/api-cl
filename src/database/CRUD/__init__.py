from src.database.CRUD import pool
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=pool)
session = Session()
