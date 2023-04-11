from dotenv import load_dotenv
import os
import urllib
from urllib.parse import quote_plus
from urllib import parse
from dotenv import load_dotenv
from os import path

from urllib.parse import urlparse

load_dotenv()
SQLALCHEMY_DATABASE = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
UPLOADED_PHOTOS_DEST = os.getenv('UPLOADED_PHOTOS_DEST')


paramsdev = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=Guilherme;"
                                 "DATABASE=BIGDATA;"
                                 "UID=sa;"
                                 "PWD=123")

SQLALCHEMY_DATABASE_URI= ("mssql+pyodbc:///?odbc_connect=%s" % paramsdev)