import scrapy
import requests
import time
import logging
import psutil
import os
import threading 
from scrapy.exporters import CsvItemExporter
from scrapy.crawler import CrawlerProcess
import datetime
# from scrapy.statscollectors import StatsCollector


proc = psutil.Process()
start_cpu_usage = psutil.cpu_percent(interval=1)
# end_time = 0
# start_time = 0
total_time = 0
total_time2 = 0

class TeamsSpider1(scrapy.Spider):
    name = 'hockey_teams'
    start_urls = []

    start_time = time.time()
    end_time = 0

    for i in range(1, 25):
        url = 'https://scrapethissite.com/pages/forms/?page_num=%s' % i
        start_urls.append(url)

    # print("CURRENT CPU >>> %i" %(this_thread.cpu_num()))
    def parse(self, response):
        for team in response.css('.team'):
            
            yield {
                'Team': team.css('.name::text').extract_first().strip(),
                'Wins': team.css('.wins::text').extract_first().strip(),
            }

    def closed(self, reason):
        end_time = time.time()
        end_cpu_usage = psutil.cpu_percent(None,percpu=True)
        self.logger.info("CPU usage >>>> %f" %end_cpu_usage[0])
        self.logger.info("CPU usage >>>> %f" %end_cpu_usage[1])
        self.logger.info("CPU usage >>>> %f" %end_cpu_usage[2])
        self.logger.info("CPU usage >>>> %f" %end_cpu_usage[3])
        print("TotalTime >>>> ") 
        
        global total_time 
        total_time += end_time - self.start_time
        print(total_time)

avg_elapsed_time = 0

for i in range(0, 1):
    process = CrawlerProcess(settings={
        "FEEDS": {
            "teams.csv": {"format": "csv"},
        },
        "LOG_LEVEL": 'INFO'
    })

    process.crawl(TeamsSpider1)
process.start()

print("AVG time2 %f"%( total_time2/3))
print("AVG time1 %f"%( total_time/5))
