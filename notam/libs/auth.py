class auth(object):
    def __init__(self, user, pwd, use):
        self.user = user
        self.pwd = pwd
        self.use = use
        self.payload = '{"username": "' + str(user) + '", "password": "' + str(pwd) + '"}'
