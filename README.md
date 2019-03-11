```
├── README.md
├── baidu
│   ├── __init__.py
│   ├── debug_settings.py (调试配置文件)
│   ├── items.py (定义的数据模型)
│   ├── middlewares.py (空的)
│   ├── pipelines.py (scrapy中的pipelines)
│   ├── prod_settings.py (生产配置文件)
│   ├── scrapy_redis_bloomfilter （适应布隆去重的spider）
│   │   ├── RedisCrawlSpider_for_search.py （针对通过关键字 爬取 问题连接的spider类）
│   │   ├── RedisCrawlSpider_for_similarity.py (针对通过 问题 爬取相似问题的spider类)
│   │   ├── __init__.py
│   └── spiders
│       ├── multi.sh (运行脚本)
│       ├── search_master.py  (针对通过关键字 爬取 问题连接的)
│       └── similarity_question_master.py (针对通过 问题 爬取相似问题的)
├── keyword.txt # 要爬取的关键词表
├── scrapy.cfg # scrapy (生成模型|调试模式)的配置文件
├── scrapy_redis #scrapy_redis的包 已经改成布隆去重了
├── select_pipelines.py select_pipelines装饰器
├── producer.py 生产者的参考代码
```

```
如何运行
启动好mysql 和 redis 
在 prod_settings.py配置好端口和密码
然后
cd spiders
sh multi.sh
```

```
如何添加新的爬取连接 
cd /container_data/mysql
vim run.py

import redis

r = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True,
                )  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
#
with open('/container_data/mysql/mini_ac',encoding='utf-8') as fp:
    for keyword in fp.readlines():
        keyword = keyword.replace('\n', '')
        r.lpush('similarity:start_urls', keyword)

修改 /container_data/mysql/mini_ac 
href.sql是全部数据
modify_href.sql 是由href.sql清洗出连接的数据
mini_aa  mini_ab  mini_ac  mini_ad  mini_ae  mini_af  mini_ag  mini_ah  mini_ai  mini_aj  mini_ak 
是由href.sql 切分出来的数据
mini_ab mini_ac 已经跑了
mini_aa 跑的时候没有去重 预计要重新跑一次
为你接下来要爬取的链接名字。 
然后运行 python3 run.py  等几分钟后 运行结束后就添加完成了
```