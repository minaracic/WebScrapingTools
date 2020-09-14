import requests
import time
from bs4 import BeautifulSoup
import psutil 
import os
import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor

NUM_OF_ITERATIONS = 10

this_thread = psutil.Process()

start_urls = []
for i in range(1, 25):
    url = 'https://scrapethissite.com/pages/forms/?page_num=%s' % i
    start_urls.append(url)

def parse(raw_page):
    soup = BeautifulSoup(raw_page, 'html.parser')
    teams = soup('tr')
    for j in range(0, len(teams)):
        team = teams[j]
        team_name = team.select_one('.name')
        wins = team.select_one('.wins')
        if(team_name and wins):
            team_name = team_name.string.strip()
            wins = wins.string.strip()
            line = team_name + ' , ' + wins + '\n'
            file.write(line)

def parse_pages(pages):
    for i in range(0, len(pages)):
        parse(pages[i])

def scrape():
    raw_pages = []
    for i in range(0, 24):
        raw_page = requests.get(start_urls[i]).text
        # return raw_page
        raw_pages.append(raw_page)
    return raw_pages
        

file = open("teams.txt","w+")

avg_total_time = 0
# sum_cpu_usage0 = 0
cpu_usage = 0

for i in range(0, NUM_OF_ITERATIONS):
    start_time = time.time()
    this_thread.cpu_percent()

    # code to test here
    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(scrape)
        
        # parse_pages(future.result())

    end_time = time.time()
    cpu_usage += this_thread.cpu_percent() / psutil.cpu_count()

    # sum_cpu_usage0 += end_cpu_usage[0]
    # sum_cpu_usage1 += end_cpu_usage[1]
    # sum_cpu_usage2 += end_cpu_usage[2]
    # sum_cpu_usage3 += end_cpu_usage[3]
    avg_total_time += end_time - start_time


print("Latency >>> %f " %(avg_total_time/NUM_OF_ITERATIONS))
print("Total cpu usage per physical cpu >>> %f " %(cpu_usage/NUM_OF_ITERATIONS))
# print("Total cpu usage 2 >>> %f " %(sum_cpu_usage1/NUM_OF_ITERATIONS))
# print("Total cpu usage 3 >>> %f " %(sum_cpu_usage2/NUM_OF_ITERATIONS))
# print("Total cpu usage 4 >>> %f " %(sum_cpu_usage3/NUM_OF_ITERATIONS))

file.close()


# memory_used = this_thread.memory_info()[0]/10**6


