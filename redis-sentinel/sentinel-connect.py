#/usr/bin/env python3
# -*- coding:utf-8 -*-
#   mail: infaaf@126.com

import redis
from redis.sentinel import Sentinel
import random
#直接连接方式
# client= redis.StrictRedis(host='192.168.1.20',port=6379,db=0,password='abc')
# res=client.get('k1').decode()
# print('直接连接方式',res)


# 哨兵连接方式： 从sentinel获取主从节点后连接   # 从redis2.8开始支持
sentinel = Sentinel([('192.168.1.20',26379),('192.168.1.21',26379),('192.168.1.22',26379)],socket_timeout=0.1)
master = sentinel.discover_master('mymaster')
slave = sentinel.discover_slaves('mymaster')
print(master)  # ('192.168.1.20', 6379)
print(slave)   # [('192.168.1.22', 6379), ('192.168.1.21', 6379)]

# 手动过程连接 （测试用）
writeclient= redis.StrictRedis(host=master[0],port=master[1],db=0,password='abc')
r= random.randrange(0,len(slave))
readclient=redis.StrictRedis(host=slave[r][0],port=slave[r][1],db=0,password='abc')
userdict={'name':'tom','type':'cat'}
writeclient.hmset('u:1',userdict)
res = readclient.hget('u:1','name').decode()
print('哨兵连接方式   clinet: {client},   res: {res}'.format(client=slave[r],res=res))

# 自动连接 （实际使用）
automaster = sentinel.master_for('mymaster', socket_timeout=0.5, password='abc', db=0)
w_ret = automaster.set('foo', 'bar')
# p=automaster.pipeline() #支持pipline

autoslave = sentinel.slave_for('mymaster', socket_timeout=0.5, password='abc', db=0)
r_ret = autoslave.get('foo')
print('自动选取从节点获取数据',r_ret)

