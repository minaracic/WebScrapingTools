import scrapy
import requests
import time
import logging
import psutil
import os

logger = logging.getLogger('mycustomlogger')
start_time = 0
end_time = 0

pid = os.getpid()
this_thread = psutil.Process(pid)
start_cpu_usage = psutil.cpu_percent(None)

class QuotesSpider(scrapy.Spider):
    start_time = time.time()
    name = 'hockey_teams'

    start_urls = [
        'https://scrapethissite.com/pages/forms/'
    ]

    for i in range(2, 25):
        url = 'https://scrapethissite.com/pages/forms/?page_num=%s' % i
        start_urls.append(url)

    def parse(self, response):
        for team in response.css('.team'):
            yield {
                'Team': team.css('.name::text').extract_first(),
                'Wins': team.css('.wins::text').extract_first(),
            }

    def closed(self, reason):
        end_cpu_usage = psutil.cpu_percent(None)
        logger.info( 'Current CPU usage >>> %f' % end_cpu_usage)
        memory_used = this_thread.memory_info()[0]/10**6
        logger.info("Memory used >>> %f" %memory_used)

    



