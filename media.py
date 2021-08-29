from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import os
import django

from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()

from scraper.models import Channel



class VideoDownloader:
    driver = webdriver.Chrome('chromedriver')
    lastkey = ""
    url = ""

    def __init__(self, profile):
        profile_name = profile.insta
        self.url = f"https://www.instagram.com/{profile_name}/"

        self.lastkey = profile.lastkey_insta

    
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
            try:
                caption = text.span.contents[0].strip()
            except:
                caption = ''
            with open(file,'wb') as f: 
                f.write(r.content)
            
            video_content = [file, caption]

            return video_content
        else:
            return None

    
    async def update_lastkey(self, new_key, profile):
        self.lastkey = new_key

        profile.lastkey_insta = new_key
        async_save = sync_to_async(profile.save)
        
        await async_save()

