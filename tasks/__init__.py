import flask
from .db import setup_db


def create_app(config=None) -> flask.Flask:
    app = flask.Flask(__name__)

    if config is not None:
        app.config["DATABASE_URI"] = config["DATABASE_URI"]
    else:
        app.config["DATABASE_URI"] = "sqlite:///tasks.db"

    engine, session = setup_db(app.config["DATABASE_URI"])
    app.db_engine = engine
    app.db_session = session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.db_session.remove()

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
