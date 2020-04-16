from pathlib import Path
from dotenv import load_dotenv
from routes import userRoute, authRoute
from mysql import mysql
from utils.errorHandler import error_handler
from werkzeug.exceptions import HTTPException
import os
from flask import Flask
import cloudinary
app = Flask(__name__)

env_path = Path('.') / '.env'
load_dotenv(
    dotenv_path=env_path)

with app.app_context():
    db = mysql.init_mysql()
    mysql.db = db

cloudinary.config(
    cloud_name=os.getenv(
        "CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv(
        "CLOUDINARY_API_KEY"),
    api_secret=os.getenv(
        "CLOUDINARY_API_SECRET")
)

app.register_blueprint(
    authRoute.auth, url_prefix='/api/v1/auth')

app.register_blueprint(
    userRoute.user, url_prefix='/api/v1/user')

app.register_error_handler(
    HTTPException, error_handler)
