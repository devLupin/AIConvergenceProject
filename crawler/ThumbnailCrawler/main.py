import urllib.request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from tqdm import tqdm

SCROLL_PAUSE_SEC = 2

num_images_limit = 200

def scroll_down():
    global driver
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            time.sleep(SCROLL_PAUSE_SEC)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            try:
                driver.find_element_by_class_name("mye4qd").click()
            except:

               if new_height == last_height:
                   break

        last_height = new_height

def make_dir(keyword):
    path = os.path.join('imgs/' + keyword)
    os.makedirs(path, exist_ok=True)

def crawling(keyword, path):
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjgwPKzqtXuAhWW62EKHRjtBvcQ_AUoAXoECBEQAw&biw=768&bih=712'.format(
        keyword)

    global driver

    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)

    time.sleep(1)

    scroll_down()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img', attrs={'class': 'rg_i Q4LuWd'})

    print('number of img tags: ', len(images))

    n = 1
    for i in tqdm(images, desc='crawling ' + keyword + '...'):

        if n > num_images_limit:
            break

        try:
            imgUrl = i["src"]
        except:
            imgUrl = i["data-src"]

        img_path = os.path.join('./imgs/', path)

        try:
            with urllib.request.urlopen(imgUrl) as f:
                with open(img_path + '/' + str(n) + '.jpg', 'wb') as h:
                    img = f.read()
                    h.write(img)
        except:
            pass

        n += 1

def main():
    os.makedirs('imgs', exist_ok=True)
    
    title = [
             ## 비공개!
             ]
    
    keywords = [
                ## 비공개!
    ]

    for i in range(len(title)):
        for k in keywords[i]:
            make_dir(k)
            crawling(title[i] + k, k)
            print(k)

if __name__ == "__main__":
	main()