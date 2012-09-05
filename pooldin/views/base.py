from flask.views import MethodView


class BaseView(MethodView):

    @classmethod
    def as_view(cls, name=None):
        name = name or getattr(cls, 'name', None)
        name = name or cls.__name__.lower()
        return super(BaseView, cls).as_view(name)

    @classmethod
    def init_app(cls, app):
        view = cls.as_view()
        cls.add_routes(app, view)

    @classmethod
    def add_routes(cls, app, view):
        pass
