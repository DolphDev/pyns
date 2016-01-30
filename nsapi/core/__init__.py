from nationstates import Api as NSApi, get_ratelimit, clear_ratelimit
#from . import exceptions

__rltracker__ = list()



class SessionWrapper():

    """
    This Class Wraps around Request.Session
    """

    def __init__(self, user_agent):
        self.session = NSApi(user_agent=user_agent)

    def get(self, api, value, shard):
        return self.session.request(api, value=value, shard=list(shard) if shard else None, auto_load=False)


class RequestObject(object):

    """
    This class wraps around SessionWrapper
    """

    def __init__(self, user_agent):
        self.session = SessionWrapper(user_agent=user_agent)

    def get(self, api, value, shard):
        return self.session.get(api, value, shard)

    @staticmethod
    def get_ratelimit():
        return get_ratelimit()


