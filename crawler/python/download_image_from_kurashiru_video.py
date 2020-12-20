import requests
from bs4 import BeautifulSoup
import lxml.html


r = requests.get(
    'https://www.kurashiru.com/search?utf8=%E2%9C%93&query=%E3%81%8B%E3%81%BC%E3%81%A1%E3%82%83'
)

print(r)
# print(r.content)

soup = BeautifulSoup(r.content, 'lxml')
dom = lxml.html.fromstring(r.content)

# print(soup.findAll('img'))
tags = soup.find_all('img', class_='compressed')

for idx, tag in enumerate(tags):
    print(idx, tag)
