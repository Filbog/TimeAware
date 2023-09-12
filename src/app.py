from flask import Flask, render_template, flash
from flask_migrate import Migrate
from flask_login import LoginManager

from models import db
from models import User

from views import views


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = "fq)4540sd#@e&&tpe6v3kjl7!w1k=7^)#6-dfmqf44m7xj"

    # # # Setting up database

    # # for local environment with SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # # for local environment with PostgreSQL - not working
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://database-postgres.db"

    # for deployment on fly.io, I guess
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = "postgresql://postgres:R17k9TrHftamjyx@timeaware-postgres-db.flycast:5432/timeaware_db.db"

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False  # Disable modification tracking

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    # we're loading the user from the database - it'll be accessible from current_user object
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # registering our blueprints

    from auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app


app = create_app()
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, port=5000, host="0.0.0.0")
