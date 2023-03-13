from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import requests
import shutil

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options=chrome_options
driver = webdriver.Chrome()
actions = ActionChains(driver)

url = 'https://pikabu.ru/community/mem'
url2 = 'https://pikabu.ru/community/Dankmemes'

driver.maximize_window()
driver.get(url)


ls = []
count = 1
cont = []
r_count = 0
for i in range(75):

    content = driver.find_elements(By.CSS_SELECTOR, 'article.story')

    for art in content:
        if art not in cont:
            content_html = art.get_attribute('innerHTML')
            soup = BeautifulSoup(content_html, features='html.parser')
            pictures = soup.select('div.story-image__content')
            try:
                p = pictures[0].find('img').get('data-large-image')

                name = p.split('/')[-1].split('.')[0]
                name_for_check = p.split('/')[-1]

                if name_for_check not in ls:
                    with open(f'images/{name}.png', 'wb') as f:
                        image = requests.get(p, stream=True)
                        shutil.copyfileobj(image.raw, f)

                        print(f'Картинка {count}, {name}.png скачалась')
                        count+=1
                    ls.append(name)
                else:
                    continue
            except IndexError:
                continue
        cont.append(art)

    driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
    sleep(3)
    print(r_count)
    r_count+=1






#new
# добавить проверку уникальности картинки по url
# спарсить несколько картинок
#<section class="stories-feed__message" style="display: block;">Отличная работа, все прочитано!</section>