import argparse
import requests
from bs4 import BeautifulSoup

_URL = 'https://www.google.co.jp/search?q=%E3%81%AA%E3%81%99&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjNoPv1k5zcAhUBw7wKHW3uAPkQ_AUICigB&biw=755&bih=662&dpr=2#imgrc=2k4c6NZkSqxbbM:'

def get_soup(url):
    response = requests.get(url)
    # print(response.text)

    return BeautifulSoup(response.content, 'lxml')

def main(url):
    soup = get_soup(url)
    print('**************** img ****************')
    images = soup.find_all('img')
    for image in images:
        print(image)

    print('**************** href ****************')
    hrefs = soup.find_all('href')
    for href in hrefs:
        print(href)

    print('**************** src ****************')
    srcs = soup.find_all('src')
    for src in srcs:
        print(src)
    

if __name__ == '__main__':
    url = _URL
    main(url)

    # parser for command line arguments
    # parser = argparse.ArgumentParser(
    #     description='parse html document'
    # )
    # parser.add_argument('--url',
    #                     dest=url,
    #                     default=None,
    #                     type=str,
    #                     help='please enter the url')
    # argv = parser.parse_args()
    
    # main(argv.url)

    
