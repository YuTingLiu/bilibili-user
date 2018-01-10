import redis
import random
import json
import re
import pandas as pd

r = redis.Redis(host='172.17.0.2', port=6379,db=2)
r.delete("last_mid_is")
datas = []
for key in r.keys():
    data  = r.hgetall(key)
    # print(len(data))
    data = {k.decode("utf-8") : (v).decode("utf-8")  for k, v in data.items()}
    datas.append(data)
print(r.dbsize())


r = redis.Redis(host='172.17.0.2', port=6379,db=3)
r.hmset("last_mid_is",{"mid":str(20)})
print(r.hgetall("last_mid_is")['mid'.encode("utf-8")].decode("utf-8"))


# {"cmd":"SEND_GIFT","data":{"giftName":"\u8fa3\u6761","num":2,' \
# '"uname":"Parrrrrris","rcost":295100705,"uid":11674627,"top_list":[{"uid":94380,' \
# '"uname":"\u72fc\u4e0e\u751c\u98df","face":"http://i2.hdslb.com/bfs/face/56ed78ac0c777bab44730732bc0ed210ae8adf75.jpg","rank":1,' \
# '"score":2410400,"guard_level":1,"isSelf":0},{"uid":889098,"uname":"CI0rHJpguwHIMZZ9",' \
# '"face":"http://i1.hdslb.com/bfs/face/d0c40aa0fdfe1e79603d98869875fc173c1aeebb.jpg","rank":2,"score":1400200,"guard_level":0,"isSelf":0},' \
# '{"uid":1928107,"uname":"\u676f\u5177\u7684\u75
