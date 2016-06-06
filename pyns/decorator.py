from .core.objects import (Shard)

def hasname(n, shardlist):
    return n in {x.name for x in shardlist}

def getshard(n, shardlist):
    for x in shardlist:
        if x.name == n:
            return x


def shardrefcalc(shardfetch, shardhas):
    namelist = {x.name for x in shardfetch | shardhas}
    for sname in namelist:
        if hasname(sname, shardfetch):
            yield getshard(sname, shardfetch)
            continue
        if hasname(sname, shardhas):
            yield getshard(sname, shardhas)
            continue


def implement_shardtrack(obj):

    @property
    def __shardref__(self):
        return set(shardrefcalc(self.__shardfetch__, self.__shardhas__))
    obj.__shardref__ = __shardref__
    obj.__shardhas__ = set()
    obj.__shardfetch__ = set()
    return obj


def default_request(kind):

    def wrapper(obj):

        def get(self):
            self.nsobj = (
                self.api_instance.r
                .get(self.__apiendpoint__, value=self.__value__, shard=list()))
            try:
                self.nsobj.load()
            except ConnectionError as err:
                raise err
            self.__shardfetch__ = self.__shardhas__
            self.__shardhas__ = self.__shardref__ | set(
                (Shard(x) for x in (self.collect().keys())))
            return self
        setattr(obj, kind, get)
        return obj
    return wrapper
