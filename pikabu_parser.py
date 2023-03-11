from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import requests
import shutil


driver = webdriver.Chrome()
actions = ActionChains(driver)

url = 'https://pikabu.ru/community/mem'


driver.get(url)

# sleep(3000)

picture_container = driver.find_element(By.CSS_SELECTOR, 'figure.story-image')
picture_container_html = picture_container.get_attribute('innerHTML')
soup = BeautifulSoup(picture_container_html, features='html.parser')

pictures = soup.select('div.story-image__content')


print(pictures)

count = 0
for picture in pictures:
    link = picture.find('img')
    img_url = link.get('data-large-image')
    name = count
    with open(f'images/{name}.png', 'wb') as f:
        image = requests.get(img_url, stream=True)
        shutil.copyfileobj(image.raw, f)

    print(f'Скачена картинка {name}')


# добавить проверку уникальности картинки по url
# спарсить несколько картинок