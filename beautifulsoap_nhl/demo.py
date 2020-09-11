import requests
import time
from bs4 import BeautifulSoup
import psutil 
import os

file = open("teams.txt","w+")
start_time = time.time()
start_urls = []
cnt = 0

pid = os.getpid()
this_thread = psutil.Process(pid)
start_cpu_usage = psutil.cpu_percent(None)

for i in range(1, 25):
    url = 'https://scrapethissite.com/pages/forms/?page_num=%s' % i
    start_urls.append(url)

for i in range(0, 24):
    raw_page = requests.get(start_urls[i]).text
    soup = BeautifulSoup(raw_page, 'html.parser')

    teams = soup('tr')
    for j in range(0, len(teams)):
        team = teams[j]
        team_name = team.select_one('.name')
        wins = team.select_one('.wins')
        if(team_name and wins):
            cnt+=1
            team_name = team_name.string.strip()
            wins = wins.string.strip()
            line = team_name + ' , ' + wins + '\n'
            file.write(line)

print("Total data scraped >>> %i" %cnt)

end_time = time.time()
print("Total time >>> %f " %(end_time - start_time))

end_cpu_usage = psutil.cpu_percent(None)
print("Current CPU usage >>> %f" % end_cpu_usage)
memory_used = this_thread.memory_info()[0]/10**6
print("Memory used >>> %f " %memory_used)

file.close()
