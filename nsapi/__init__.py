try:
    from objects import (Nation, Region, WorldApi, WorldAssemblyApi, Shard)
    from core import RequestObject
except ImportError:
    from .core import RequestObject
    from .objects import (Nation, Region,
                          WorldApi, WorldAssemblyApi,Shard)



class Api(object):

    def __init__(self, user_agent=None, apiversion="7"):
        """Creates Api Instance"""

        self.r = RequestObject(user_agent=user_agent)
        self.version = apiversion
        self.user_agent = user_agent

    def nation(self, nation):
        return Nation(self, nation)

    def region(self, region):
        return Region(self, region)

    def wa(self, council):
        return WorldAssemblyApi(self, council)

    def world(self):
        return WorldApi(self)



#for x in Api("nsapi testing").get_world().region.nations:
#    break
#    print(x)
