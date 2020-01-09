import requests
from bs4 import BeautifulSoup
import csv

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.content, 'lxml')

links = soup.select('.storylink')
subtext = soup.select('.subtext')

def sorted_stories(updated_list): # sorting by votes in ascending order
  return sorted(updated_list, key= lambda k:k['no_of_votes'], reverse=True)

def get_stories(links, subtext):
  full_updates = []
  for key, values in enumerate(links):
    title = values.getText()
    href = values.get('href', None)
    votes = subtext[key].select('.score')
    if len(votes): # if length of the vote is not zero 
      vote = int(votes[0].getText().replace(' points', '')) # replacing the text part with the empty strings
      if vote > 50:
        full_updates.append({'title': title, 'links': href, 'no_of_votes': vote})
  return sorted_stories(full_updates)

def write_to_csv(filename, datas):
    with open(filename, 'w', newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)
 
datas = get_stories(links, subtext)
write_to_csv("news_stories.csv", datas)
