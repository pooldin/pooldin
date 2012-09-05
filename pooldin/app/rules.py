class RulesMixin(object):

    def add_get_rule(self, *args, **kw):
        kw['methods'] = ['GET']
        return self.add_url_rule(*args, **kw)

    def add_post_rule(self, *args, **kw):
        kw['methods'] = ['POST']
        return self.add_url_rule(*args, **kw)

    def add_put_rule(self, *args, **kw):
        kw['methods'] = ['PUT']
        return self.add_url_rule(*args, **kw)

    def add_patch_rule(self, *args, **kw):
        kw['methods'] = ['PATCH']
        return self.add_url_rule(*args, **kw)

    def add_delete_rule(self, *args, **kw):
        kw['methods'] = ['DELETE']
        return self.add_url_rule(*args, **kw)
