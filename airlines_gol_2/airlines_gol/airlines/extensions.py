import logging
import requests
from scrapy import signals
from scrapy.exceptions import NotConfigured
logger = logging.getLogger(__name__)


class Telegram:

    def __init__(self, item_count=0):
        self.item_count = 0
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        ext = cls(0)
        
        # connect the extension object to signals
        #crawler.signals.connect(ext.engine_fim, signal=signals.engine_stopped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        
        # return the extension object
        return ext
        
    def spider_closed(self, spider):
        stats = spider.crawler.stats.get_value('item_scraped_count')
        self.item_scraped=+stats
        return self.dispara_log()
 
        
    # def dispara_log(self):
    #     #token="5049169271:AAFS8d91uQzfRrHaUY-M4OQ4ZKfaqkMTmA8"
    #     url = "https://api.telegram.org/bot{}/sendMessage".format(token)
    #     id="ENTER ID"
    #     text= "Crawler AirLinesGol Exportado um total de: "+str(self.item_scraped)
    #     data={"chat_id":id,"text":text}

    #     requests.post(url,data)
    
    
    def engine_fim(self):
        logger.info("----------------------------------ENGINEPAROUUU---------------------------")
        self.dispara_log() 
        
      