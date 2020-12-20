import time
import argparse

from selenium import webdriver
import urllib.error
import urllib.request

_URL = 'https://www.google.com/search?q=%E5%A4%A7%E7%90%86%E7%9F%B3+%E7%99%BD&rlz=1C1CHBD_en-GBJP826JP826&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiuma_dnfDjAhXUKqYKHYAKA40Q_AUIECgB&biw=1920&bih=888'


def download_image(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode='wb') as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)
        
    return


def main():
    url = _URL
    
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.implicitly_wait(100)
    driver.get(url)

    for i in range(5):
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);'
        )
        time.sleep(2)
        
    more_image_button = driver.find_element_by_id('smb')
    more_image_button.click()
    time.sleep(2)
    
    for i in range(5):
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);'
        )
        time.sleep(2)
    time.sleep(5)

    images = driver.find_elements_by_xpath('//img')
    
    for idx, image in enumerate(images):

        print(idx)
        url = image.get_attribute('src')
        data_url = image.get_attribute('data-src')
        padding_number = '{0:03d}'.format(idx)
        dst_path = 'data/' + str(idx) + '.png'
        
        try:
            if url is not None:
                download_image(url, dst_path)
            else:
                download_image(data_url, dst_path)
        except AttributeError:
            print(url)
            pass
        except ValueError:
            print(url)
            pass


if __name__ == '__main__':
    main()
    # TODO
    # parser = argparse.ArgumentParser(
    #     description='scraping from web url'
    # )
    # parser.add_argument('--url',
    #                     dest='url',
    #                     default=None,
    #                     type=str,
    #                     help='please enter the url adress')
    # argv = parser.parse_args()
    # main(argv.url)
