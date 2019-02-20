from scrapy.exceptions import DropItem

def check_spider_pipeline(name_list):
    def decorator(process_item_method):
        def wrapper(self, item, spider):
            if spider.name in name_list:
                return process_item_method(self, item, spider)
            else:
                return item
        return wrapper

    return decorator

