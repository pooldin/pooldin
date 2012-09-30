import os
import sys
import cdecimal
sys.modules["decimal"] = cdecimal


path = os.path.abspath(__name__)


def create_app():
    from .app import App
    app = App(__name__)
    app.init()
    return app
