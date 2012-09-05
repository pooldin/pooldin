import os

path = os.path.abspath(__name__)


def create_app():
    from .app import App
    app = App(__name__)
    app.init()
    return app
