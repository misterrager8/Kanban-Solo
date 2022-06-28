import dotenv
import os

dotenv.load_dotenv()

ENV = os.getenv("ENV")
DEBUG = os.getenv("DEBUG")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
