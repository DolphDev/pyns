from nationstates import Shard

class Shard(Shard):

    def __eq__(self, n):
        return n._get_main_value() == self._get_main_value()

    def __hash__(self):
        return hash(self.__class__) ^ hash(self._get_main_value())
