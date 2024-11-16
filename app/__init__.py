import flask


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)

    app.tasks = []

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
