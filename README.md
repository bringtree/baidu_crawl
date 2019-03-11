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
```

```
如何运行
启动好mysql 和 redis 
在 prod_settings.py配置好端口和密码
然后
cd spiders
sh multi.sh
```

