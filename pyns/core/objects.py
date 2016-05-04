from nationstates import Shard as _Shard
from nationstates.NScore.bs4parser import NSDict

class NSBaseObject(object):
    pass


class Shard(_Shard):

    """While usaully we want to shards with different params
    to be different objects (Not ==), The api and therefore this module
    doesnt work that way. Each request can only have 1 of each shard.
    """

    def __eq__(self, n):
        if n.__class__ == self.__class__:
            return n._get_main_value() == self._get_main_value()
        return False

    def __hash__(self):

        return hash(self.__class__) ^ hash(self._get_main_value())


class APIObject(NSBaseObject):

    """
    Base Objects for Objects that Represent a API
    """

    def __init__(self, api_instance):
        raise NotImplementedError

    def __getattr__(self, attr):
        """Allows dynamic access to Nationstates shards"""

        if not isinstance(attr, Shard):
            attr = Shard(attr)
        if attr in self.__shardhas__:
            return self.collect()[attr.name]
        try:
            if attr in self.__shardfetch__:
                self.execute()
                return self.collect()[attr.name]
            else:
                self.fetch(attr)
                self.execute()
                return self.collect()[attr.name]
        except KeyError:
            self.__shardhas__.remove(attr)
            raise AttributeError('{attrmessage}'.format(
                shard=attr,
                attrmessage=('\'%s\' has no attribute \'%s\'' % (
                    type(self), attr))))

    def __getitem__(self, attr):
        self.fetch(attr)
        return self

    def __repr__(self):
        return "<{objectname}:{value} at {id}>".format(
            objectname=self.__class__.__name__,
            value=self.__value__,
            id=str(hex(id(self))).upper()
        )

    def __dir__(self):
        return dir(super(NSBaseObject, self)) + [x.name for x in self.__shardref__]

    def fetch(self, *shards):
        for shard in shards:
            if (
                not (isinstance(shard, _Shard)
                     or isinstance(shard, Shard)
                     or isinstance(shard, str))):
                raise TypeError("Shard can't be Type({})".format(type(shard)))
        self.__shardfetch__ = set(
            [Shard(shard) if isinstance(shard, str)
             else (Shard(shard.name,
                         **{key[0][1]:key[1][1] for (key) in [
                             sorted(list(shard.items()))
                             for shard in shard._tags]})
                   if (isinstance(shard, _Shard)
                       or isinstance(shard, Shard))
                   else shard)
             for shard in shards]) | self.__shardfetch__

        return self

    def get(self, *args):
        self.fetch(*args)
        return self.execute()

    def group(self, *args):
        self.get(*args)
        argstring = [x.name if not isinstance(x, str) else x for x in args]
        return NSDict({x:self.collect()[x] for x in argstring})

    def needsfetch(self, shard):
        if not self.has_shard(shard):
            self.fetch(shard)
            self.execute()
        return self

    def collect(self):
        return self.nsobj.collect()

    def has_fetch(self, shard):
        return shard in self.__shardfetch__

    def has_shard(self, shard):
        if not isinstance(shard, Shard):
            shard = Shard(shard)
            return shard in self.__shardhas__

    def execute(self):
        self.nsobj = (
            self.api_instance.r
            .get(self.__apiendpoint__, value=self.__value__,
                 shard=self.__shardref__)
        )
        self.__shardhas__ = self.__shardref__
        self.__shardfetch__ = set()
        try:
            self.nsobj.load()
        except ConnectionError as err:
            raise err
        return self

    def refresh(self):
        self.execute()
        return self

    @property
    def __value__(self):
        raise NotImplementedError

    def __gen__(self, cls, val, splitval):
        for item in self.collect().get(val).split(splitval):
            yield cls(self.api_instance, item)
