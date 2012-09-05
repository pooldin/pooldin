class InitMixin(object):

    def init(self):
        self.init_extensions()
        self.init_middleware()
        self.init_processors()
        self.init_routes()
        self.init_blueprints()
        self.init_env()
        return self

    def init_extensions(self):
        pass

    def init_middleware(self):
        pass

    def init_processors(self):
        pass

    def init_routes(self):
        if hasattr(self, 'views'):
            self.init_views(self.views)

    def init_blueprints(self):
        pass

    def init_env(self):
        if hasattr(self, 'env') and \
                hasattr(self, 'init_%s' % self.env):
            getattr(self, 'init_%s' % self.env)()

    def init_views(self, views):
        views = views or []

        for view in views:
            view.init_app(self)
