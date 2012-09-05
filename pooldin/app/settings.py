class base(object):
    DEBUG = False
    TESTING = False


class dev(base):
    DEBUG = True
    TESTING = True
    ASSETS_DEBUG = "merge"


class test(base):
    TESTING = True


class prod(base):
    pass
