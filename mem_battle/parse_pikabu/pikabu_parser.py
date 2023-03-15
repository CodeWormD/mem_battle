from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import requests
import shutil


from mems.models import Mem




def load_browser(url):

    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    # chrome_options=chrome_options

    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.maximize_window()
    driver.get(url)

    return driver


def parse_pikabu(driver):

    list_check = [] # append names for to avoid repeat
    count_images = 1 # count images
    ls_for_windows = []
    count_windows_scrolled = 0

    TIME_SLEEP = 3

    while True:

        stop = count_images # if no new images downloaded - stop script

        content = driver.find_elements(By.CSS_SELECTOR, 'article.story')

        print(count_windows_scrolled)
        count_windows_scrolled+=1

        for art in content:
            if art not in ls_for_windows:
                content_html = art.get_attribute('innerHTML')
                soup = BeautifulSoup(content_html, features='html.parser')
                pictures = soup.select('div.story-image__content')

                try:
                    p = pictures[0].find('img').get('data-large-image')

                    name = p.split('/')[-1].split('.')[0]
                    name_for_check = p.split('/')[-1]

                    if name_for_check not in list_check:
                        with open(f'images/{name}.png', 'wb') as f:
                            image = requests.get(p, stream=True)
                            Mem.objects.create(image=image)
                            # shutil.copyfileobj(image.raw, f)

                            print(f'Картинка {count_images}, {name}.png скачалась')
                            count_images +=1
                        list_check.append(name)
                    else:
                        continue
                except IndexError:
                    continue

            ls_for_windows.append(art)

        driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
        sleep(TIME_SLEEP)

        # check for new images
        if stop == count_images:
            break
        else:
            continue


if __name__ == '__main__':

    url = 'https://pikabu.ru/community/mem'
    url2 = 'https://pikabu.ru/community/Dankmemes'

    parse_pikabu(load_browser(url))