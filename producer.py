import redis
# mini_aa 文件样式
# url+10*&+cur_page
# http://zhidao.baidu.com/question/100337164.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/1049247881764239219.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/108932129.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/110770619.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/1112048179961457179.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/1175027067114670499.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/1238362701528688659.html&&&&&&&&&&1
# http://zhidao.baidu.com/question/133020725.html&&&&&&&&&&1

r = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True,
                )  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379

mini_list = ['e', 'f', 'g', 'h', 'i', 'j', 'k']
for file_char in mini_list:
    with open('/container_data/mysql/mini_a' + file_char, encoding='utf-8') as fp:
        for keyword in fp.readlines():
            keyword = keyword.replace('\n', '')
            r.lpush('similarity:start_urls', keyword)
