def implement_shardtrack(obj):

    @property
    def __shardref__(self):
        return self.__shardfetch__ | self.__shardhas__
    obj.__shardref__ = __shardref__
    obj.__shardhas__ = set()
    obj.__shardfetch__ = set()
    return obj

def implement_nationobject(obj):
    return obj
