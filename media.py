from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import os

from aiogram.utils.markdown import link


class VideoDownloader:
    url = 'https://www.instagram.com/group_dalnoboi/'
    driver = webdriver.Chrome('chromedriver')
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    
    def new_videos(self):
        new = []

        self.driver.get(self.url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        media_list = soup.find_all('div', class_='v1Nh3')
        for media in media_list:
            if media.a['href'] != self.lastkey:
                new.append(media.a['href'])
            else:
                break

        return new


    def download_video(self, uri):
        media_url = 'https://www.instagram.com' + uri
        self.driver.get(media_url)
        media_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        video = media_soup.find('video', class_='tWeCl')
        text = media_soup.find('div', class_='C4VMK')

        if(video):
            video_url = video['src']

            r = requests.get(video_url)

            file = "instagram_video.mp4"
            caption = text.span.contents[0].strip() + '\n' + link('Дневник Дальнобойщика', 'https://t.me/dalnob0/')
            with open(file,'wb') as f: 
                f.write(r.content)
            
            video_content = [file, caption]

            return video_content
        else:
            return None


    def get_lastkey(self):
        self.driver.get(self.url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        media_list = soup.find_all('div', class_='v1Nh3')

        return media_list[-1].a['href']

    
    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key



# url = 'https://www.instagram.com/p/CQIRuVyiQFo/'
# driver = webdriver.Chrome('chromedriver')
# driver.get(url)
# media_soup = BeautifulSoup(driver.page_source, 'lxml')
# text = media_soup.find('div', class_='C4VMK')

# print(text.span.contents[0].strip())