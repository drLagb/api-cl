from os import path, getenv
from dotenv import load_dotenv

filesPath = path.join(path.dirname(path.abspath(__file__)), "..", "..", "Files")
imagesPath = path.join(path.dirname(path.abspath(__file__)), "..", "..", "Images")
product = getenv("PRODUCT")
if not product and path.exists(path.join(path.dirname(path.abspath(__file__)), "..", "..", ".env")):
    load_dotenv(path.join(path.dirname(path.abspath(__file__)), "..", "..", ".env"))
fiat = getenv("FIAT")
integrityKey = getenv("INTEGRITY_KEY")
minBuyValue = float(getenv("MINBUY") if getenv("MINBUY") else 59000)
db_user = getenv("DB_USER") 
db_pass = getenv("DB_PASS")
db_name = getenv("DB_NAME")
db_port = getenv("DB_PORT")
db_host = getenv(
    "INSTANCE_HOST"
)