from nationstates import Shard as _Shard

try:
    import decorator
    from core.exceptions import InvalidShard, InvalidTag
    from core.objects import APIObject
    from shardobjects import Shard
except ImportError:
    from . import decorator
    from .core.exceptions import InvalidShard, InvalidTag
    from .core.objects import APIObject
    from .shardobjects import Shard



@decorator.default_request("default_request")
@decorator.implement_shardtrack
class Nation(APIObject):

    def __init__(self, api_instance, nation):
        self.__nation__ = nation
        self.__apiendpoint__ = "nation"
        self.api_instance = api_instance
        self.nsobj = api_instance.r.get(
            self.__apiendpoint__, self.__value__, set())

    @property
    def nationname(self):
        return self.__value__

    def can_recruit(self, fromregion=None):
        if fromregion:
            self.needsfetch(Shard("tgcanrecruit", fromregion=fromregion))
        else:
            self.needsfetch("tgcanrecruit")
        return bool(int(self.tgcanrecruit))

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

@decorator.default_request("default_request")
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
        return self.__gen__(Nation, "nations", ":")

    @property
    def regionname(self):
        return self.__value__

    @property
    def __value__(self):
        return self.__region__

    @__value__.setter
    def __value__(self, val):
        self.__region__ = val


@decorator.implement_shardtrack
class WorldAssemblyApi(APIObject):

    def __init__(self, api_instance, council):
        self.__council__ = council
        self.__apiendpoint__ = "wa"
        self.api_instance = api_instance
        self.nsobj = api_instance.r.get(
            self.__apiendpoint__, self.__value__, set())

    @property
    def members(self):
        self.needsfetch("members")
        return self.__gen__(Nation, "members", ",")

    @property
    def __value__(self):
        return self.__council__

    @__value__.setter
    def __value__(self, val):
        self.__council__ = val


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
        self.fetch(shard)
        self.execute()
        return self.__genrbt__(Region, "regions", ',')

    @property
    def newnations(self):
        self.needsfetch("newnations")
        return self.__gen__(Nation, "newnations", ',')

    @property
    def __value__(self):
        return self.__world__

    def __genrbt__(self, cls, val, splitval):
        # Slightly specialized for regionsbytag
        try:
            for item in self.collect().get(val).split(splitval):
                yield cls(self.api_instance, item)
        except AttributeError:
            # Replace with invalid shard
            raise InvalidTag(
                "Invalid Tag: Check your tags, the nationstates api did not return a valid response.")
