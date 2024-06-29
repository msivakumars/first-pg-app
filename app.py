from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
from db import db
from resources.employee import blp as employee_blue_print
import os


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_VERSION"] = "v1"
    app.config["API_TITLE"] = "My First Postgres Database App"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    api.register_blueprint(blp=employee_blue_print)
    return app

