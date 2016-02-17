def implement_shardtrack(obj):

    @property
    def __shardref__(self):
        return self.__shardfetch__ | self.__shardhas__
    obj.__shardref__ = __shardref__
    obj.__shardhas__ = set()
    obj.__shardfetch__ = set()
    return obj

def default_request(kind):

    def wrapper(obj):

        def get(self):
            self.execute()
            self.__shardhas__ = self.__shardhas__ | set(self.collect().keys())
            return self
        setattr(obj, kind, get)
        return obj
    return wrapper