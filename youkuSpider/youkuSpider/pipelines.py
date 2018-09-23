# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class YoukuspiderPipeline(object):
    def open_spider(self, spider):
        self.r = redis.Redis(host="127.0.0.1", port=6379, db=5)

    def process_item(self, item, spider):
        self.r.set(name=item.get("name"), value=item.get("view_json"))
        print("write success")
        return item
