import flask


def create_app():
    app = flask.Flask(__name__)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
