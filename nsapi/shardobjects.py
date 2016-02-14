from nationstates import Shard


class Shard(Shard):

    """While usaully we want to shards with different params to be different, 
    The api, and therefore this module doesnt work that way.
    """

    def __eq__(self, n):
        if n.__class__ == self.__class__:
            return n._get_main_value() == self._get_main_value()
        return False

    def __hash__(self):

        return hash(self.__class__) ^ hash(self._get_main_value())

