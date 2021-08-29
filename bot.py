import asyncio
import aioschedule
import logging

from aiogram import Dispatcher, Bot, executor
from aiogram.utils.markdown import link

from media import VideoDownloader

from asgiref.sync import sync_to_async

# Setup django
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()

from scraper.models import Channel

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = '1988732430:AAEHiVTWHHyQJSpyY8PH0JF-YvZDemVbXwI'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# Send videos
async def send_media(channel, profile):
    vd = VideoDownloader(profile)

    new_videos = vd.new_videos()
    print('Found new videos')
    if(new_videos):
        new_videos.reverse()
        for nv in new_videos:
            video = vd.download_video(nv)
            if(video):
                print('Downloading video')
                caption = video[1] + '\n' + link('Подписывайтесь', 'https://t.me/' + channel.channel_name + '/')
                with open(video[0], 'rb') as v:
                    print('Sending video')
                    print(channel.channel_name)
                    await bot.send_video(str('@' + channel.channel_name), v, caption=caption, parse_mode='markdown')
                    print('Video sent')
    
            await vd.update_lastkey(nv, profile)
            print('Lastkey updated')


# Get the llist of channels where videos are sent
async def get_channels():
    channels = await sync_to_async(list)(Channel.objects.all())

    return channels


# Get the list of instagram profiles from which videos are got
async def get_profiles(channel):
    profiles = await sync_to_async(list)(channel.get_profiles())

    return profiles


# Process
async def process_post():
    channels = await get_channels()
    print(channels)
    for channel in channels:
        if channel.is_active:
            profiles = await get_profiles(channel)
            print(profiles)
            for profile in profiles:
                await send_media(channel, profile)


async def scheduler():
    aioschedule.every().day.at("08:00").do(process_post)
    aioschedule.every().day.at("09:30").do(process_post)
    aioschedule.every().day.at("12:00").do(process_post)
    aioschedule.every().day.at("14:00").do(process_post)
    aioschedule.every().day.at("18:00").do(process_post)
    aioschedule.every().day.at("22:00").do(process_post)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(_):
    await asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)