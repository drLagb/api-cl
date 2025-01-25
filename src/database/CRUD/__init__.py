from src.database import pool
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=pool)
session = Session()
