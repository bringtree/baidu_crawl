import redis

r = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True,
                )  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
#
with open('/container_data/mysql/mini_hrefaa',encoding='utf-8') as fp:
    for keyword in fp.readlines():
        keyword = keyword.replace('\n', '')
        r.lpush('similarity:start_urls', keyword)
