try:
    import decorator
    from core.exceptions import InvalidShard
    from shardobjects import Shard
except ImportError:
    from . import decorator
    from .core.exceptions import InvalidShard
    from .shardobjects import Shard


class NSBaseObject(object):
    pass

class ShardObject(NSBaseObject):
    pass


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
            raise InvalidShard('\'{shard}\' was not returned by the Nationstates API. If not a shard request {attrmessage}'.format(
                shard=attr, attrmessage=('\'%s\' has no attribute \'%s\'' % (type(self),
                                                                             attr))))

    def __repr__(self):
        return "<{objectname}:{nationname} at {id}>".format(
            objectname=self.__class__.__name__,
            nationname=self.__value__,
            id=(hex(id(self))).upper()
        )

    def fetch(self, *shards):
        self.__shardfetch__ = set(
            [Shard(shard) if not isinstance(shard, Shard)
             else shard for shard in shards]) | self.__shardfetch__
        return self

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
        return shard in self.__shardhas__

    def execute(self):
        self.nsobj = self.api_instance.r.get(self.__apiendpoint__,
                                             value=self.__value__,
                                             shard=self.__shardref__)
        self.__shardhas__ = self.__shardref__
        self.__shardfetch__ = set()
        self.nsobj.load()
        return self

    def refresh(self):
        self.execute()
        return self

    @property
    def __value__(self):
        raise NotImplementedError


@decorator.implement_shardtrack
class Nation(APIObject):

    def __init__(self, api_instance, nation):
        self.__nation__ = nation
        self.__apiendpoint__ = "nation"
        self.api_instance = api_instance
        self.nsobj = api_instance.r.get(
            self.__apiendpoint__, self.__value__, set())

    @property
    def region(self):
        self.needsfetch("region")
        return Region(self.api_instance, self.collect().region)

    @property
    def __value__(self):
        return self.__nation__

    @__value__.setter
    def __value__(self, val):
        self.__nation__ = val


@decorator.implement_shardtrack
class Region(APIObject):

    def __init__(self, api_instance, region):
        self.__region__ = region
        self.__apiendpoint__ = "region"
        self.api_instance = api_instance
        self.nsobj = api_instance.r.get(
            self.__apiendpoint__, self.__value__, set())

    @property
    def nations(self):
        self.needsfetch("nations")
        for nation in self.collect().get("nations").split(":"):
            yield (Nation(self.api_instance, nation))

    @property
    def __value__(self):
        return self.__region__

    @__value__.setter
    def __value__(self, val):
        self.__region__ = val


@decorator.implement_shardtrack
class WorldAssemblyApi(APIObject):
    pass


@decorator.implement_shardtrack
class WorldApi(APIObject):

    def __init__(self, api_instance):
        self.__world__ = None
        self.__apiendpoint__ = "world"
        self.api_instance = api_instance
        self.nsobj = api_instance.r.get(
            self.__apiendpoint__, self.__value__, set())

    @property
    def featuredregion(self):
        self.needsfetch("featuredregion")
        return Region(self.api_instance, self.collect().get("featuredregion"))

    def regionsbytag(self, **kwargs):
        taggen = sorted(["{bool}{key}".format(
            key=x, bool="-" if y is False else "")
            for x, y in kwargs.items()])
        string = (','.join(taggen))
        shard = Shard("regionsbytag", tags=string)
        self.needsfetch(shard)
        for region in self.collect().regions.split(","):
            yield Region(self.api_instance, region)

    @property
    def __value__(self):
        return self.__world__
