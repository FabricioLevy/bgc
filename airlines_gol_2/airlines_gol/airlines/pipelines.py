# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import boto3
import json


class AirlinesPipeline:
    def process_item(self, item, spider):
        return item

class EventBridgePipeline:

    def open_spider(self, spider):
        self.client = boto3.client('events')
    
    def process_item(self, item, spider):

        eventbridge_event = {
            'Source': 'lambda',
            'Detail': json.dumps(ItemAdapter(item).asdict()),
            'DetailType': 'airlines_gol',
            'EventBusName': ''
        }

        self.client.put_events(
            Entries = [
                eventbridge_event
            ]
        )

        return item
