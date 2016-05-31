import pyns

api = pyns.Api("Testing out PYNS")

n = list(api.world().featuredregion.nations)[:5]


for x in n:
	print(x.nationname, x.can_recruit("10000 islands"))
	print((x.nsobj.api_mother.xrls))

