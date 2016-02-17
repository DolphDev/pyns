from nationstates import Shard

"""All that represent a Shard or a response that needs to be wrapped around"""


def get(d, *args):
    for arg in args:
        d = d.get(arg)
    return d

class Shard(Shard):

    """While usaully we want to shards with different params to be different objects (Not ==), 
    The api and therefore this module doesnt work that way.
    Each request can only have 1 of each shard.
    """

    def __eq__(self, n):
        if n.__class__ == self.__class__:
            return n._get_main_value() == self._get_main_value()
        return False

    def __hash__(self):

        return hash(self.__class__) ^ hash(self._get_main_value())

"""Group Shard Objects"""

class ShardObjectBase(object):
    def __init__(self, api, cls):
        self.api = api
        self.cls = api

    def Constructer(self):
        pass

    def __iter__(self, cls, *args):
        for x in get(*args):
            yield cls(x, self.api)

class DispatchList(ShardObjectBase):
    
    def __iter__(self):
        for v in self.api.cls.collect().dispatchlist.dispatch:
            yield Dispatch(v)

    def __len__(self):
        return len(list(self))

class Deaths(object):

    def __iter__(self):
        for v in self.api.cls.collect().dispatchlist.dispatch:
            yield Cause(v)

class Cause(object):
    pass

