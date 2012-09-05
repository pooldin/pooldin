class base(object):
    DEBUG = False
    TESTING = False


class dev(base):
    DEBUG = True
    TESTING = True


class test(base):
    TESTING = True


class prod(base):
    pass
