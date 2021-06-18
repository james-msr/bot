import asyncio
import aioschedule
import logging

from aiogram import Dispatcher, Bot, executor
from aiogram.utils.markdown import link

from media import VideoDownloader, channels_list, profiles_list

# from sqlighter import SQLighter

# import os
# import django


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
# django.setup()

# from scraper.models import Channel

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = '1810785353:AAH-B0PyPYT-1n_KZR-rcAl5gYA7iEcEicA'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# db = SQLighter('db.sqlite3')



async def process_post():
    

    channels = channels_list()
    for channel in await channels:
        if channel.is_active:
            profiles = profiles_list(channel)
            for profile in await profiles:
                vd = VideoDownloader(profile)

                new_videos = vd.new_videos()
                if(new_videos):
                    new_videos.reverse()
                    for nv in new_videos:
                        video = vd.download_video(nv)
                        if(video):
                            caption = video[1] + '\n' + link('Дневник Дальнобойщика', 'https://t.me/' + channel.channel_name[1:] + '/')
                            with open(video[0], 'rb') as v:
                                await bot.send_video(channel.channel_name, v, caption=caption, parse_mode='markdown')
				
                    vd.update_lastkey(nv, profile)

async def scheduler():
    aioschedule.every().day.at("08:00").do(process_post)
    aioschedule.every().day.at("09:30").do(process_post)
    aioschedule.every().day.at("10:30").do(process_post)
    aioschedule.every().day.at("17:54").do(process_post)
    aioschedule.every().day.at("18:00").do(process_post)
    aioschedule.every().day.at("22:00").do(process_post)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)