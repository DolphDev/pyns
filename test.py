import pyns

api = pyns.Api("")

n =((api.nation("grub")))
n.can_recruit(fromregion="10000 islands")
print(n.collect())