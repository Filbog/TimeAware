from flask import Flask, render_template, flash
from flask_migrate import Migrate
from flask_login import LoginManager

from models import db
from models import User, Activity


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = "fq)4540sd#@e&&tpe6v3kjl7!w1k=7^)#6-dfmqf44m7xj"

    # Setting up database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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
    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)