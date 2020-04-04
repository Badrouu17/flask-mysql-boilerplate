from pathlib import Path
from dotenv import load_dotenv
from routes import userRoute
from flask import Flask
app = Flask(__name__)

app.register_blueprint(userRoute.user, url_prefix='/user')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


@app.route('/')
def hello_world():
    return 'Hello, World!'
