import redis

r = redis.Redis(host='0.0.0.0', port=6380, decode_responses=True,
                password=123456)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379

with open('../keyword.txt') as fp:
    for keyword in fp.readlines():
        keyword = keyword.replace('\n', '')
        url = keyword + '&&&&&&&&&&1'
        r.lpush('search:start_urls', url)

