

# time_mem = driver.find_element(By.CSS_SELECTOR, 'div.story__user')
# a = time_mem.get_attribute('innerHTML')
# soup2 = BeautifulSoup(a, features='html.parser')

# t = soup2.select('div')
# tt = t[0].find('time').get('datetime')

# print(type(tt))


#         picture_container = driver.find_element(By.CSS_SELECTOR, 'figure.story-image')

#         picture_container_html = picture_container.get_attribute('innerHTML')
#         soup = BeautifulSoup(picture_container_html, features='html.parser')

#         pictures = soup.select('div.story-image__content')





# for picture in pictures:
#             link = picture.find('img')
#             img_url = link.get('data-large-image')
#             name = count
#             with open(f'images/{name}.png', 'wb') as f:
#                 image = requests.get(img_url, stream=True)
#                 shutil.copyfileobj(image.raw, f)

#             print(f'Скачена картинка {name}')
#             sleep(3000)


# st = 'name/1234567.png'
# ls = st.split('/')[-1].split('.')[0]
# print(ls)