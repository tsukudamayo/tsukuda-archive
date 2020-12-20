import time
import argparse

import urllib.request
import urllib.error

import requests
from bs4 import BeautifulSoup
import lxml.html


_URL = 'https://www.kurashiru.com/search?utf8=%E2%9C%93&query=%E3%81%AB%E3%82%93%E3%81%98%E3%82%93'


def main():
    url = _URL
    r = requests.get(url)
    
    print(r)
    # print(r.content)
    
    soup = BeautifulSoup(r.content, 'lxml')
    dom = lxml.html.fromstring(r.content)
    
    for i in range(50):
        _xpath = dom.xpath(
            '//*[@id="left_content"]/div/div[{}]/a/img'\
            .format(str(i+1))\
            .encode('utf-8')
        )
        
        for path in _xpath:
            print(path.get('alt'))
            print(path.get('src'))
            path_src = path.get('src').split('compressed')[0]
            print('video src', path_src)
            path_src = path_src + 'webm.webm'
            dst_path = './data/video/' + str(i) + '.webm'
            print('path_src', path_src)
            print('dst_path', dst_path)
    
            try:
                mov = urllib.request.urlopen(path_src).read()
                with open(dst_path, mode='wb') as f:
                    f.write(mov)
            except ValueError:
                print('invalid url')
                pass


if __name__ == '__main__':
    main()
