#/usr/bin/env python3
# -*- coding:utf-8 -*-
#   mail: infaaf@126.com

# 慢，待调试

from rediscluster import StrictRedisCluster

def redis_cluster():
    redis_nodes = [{'host': '192.168.1.21', 'port': 7000},
                   {'host': '192.168.1.21', 'port': 7001},
                   {'host': '192.168.1.21', 'port': 7002},
                   {'host': '192.168.1.21', 'port': 7003},
                   {'host': '192.168.1.21', 'port': 7004},
                   {'host': '192.168.1.21', 'port': 7005}
                   ]
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception as e:
        print("Connect Error!",e)
        return 0

    redisconn.set('name', 'admin')
    print("name is: ", redisconn.get('name'))


redis_cluster()

