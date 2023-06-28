from flask import Flask, render_template
from flask_migrate import Migrate

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

    @app.route("/")
    def hello():
        users = User.query.all()
        # for user in users:
        #     print(f"ID: {user.id}, Email: {user.email}, First Name: {user.firstName}")
        return render_template("index.html", users=users)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
