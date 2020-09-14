import requests
import time
from bs4 import BeautifulSoup
import psutil 
import os

NUM_OF_ITERATIONS = 10

pid = os.getpid()
this_thread = psutil.Process(pid)
# print("CPU USAGE >>> %f" %this_thread.cpu_percent())

start_urls = []
for i in range(1, 25):
    url = 'https://scrapethissite.com/pages/forms/?page_num=%s' % i
    start_urls.append(url)

def scrape():
    for i in range(0, 24):
        raw_page = requests.get(start_urls[i]).text
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


file = open("teams.txt","w+")

avg_total_time = 0
# sum_cpu_usage0 = 0
# sum_cpu_usage1 = 0
# sum_cpu_usage2 = 0
# sum_cpu_usage3 = 0
total_cpu_usage = 0

for i in range(0, NUM_OF_ITERATIONS):
    start_time = time.time()
    start_cpu_usage = this_thread.cpu_percent()

    scrape()

    end_time = time.time()
    total_cpu_usage += this_thread.cpu_percent() / psutil.cpu_count()
    avg_total_time += end_time - start_time


print("Latency >>> %f " %(avg_total_time/NUM_OF_ITERATIONS))
print("Total cpu usage per physical cpu >>> %f " %(total_cpu_usage/NUM_OF_ITERATIONS))

file.close()


# memory_used = this_thread.memory_info()[0]/10**6
# print("Memory used >>> %f " %memory_used)


