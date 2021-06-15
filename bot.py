import asyncio
import aioschedule
import logging

from aiogram import Dispatcher, Bot, executor

from media import VideoDownloader

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = '<Bot token>'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

vd = VideoDownloader("lastkey.txt")


async def process_post():
    new_videos = vd.new_videos()

    if(new_videos):
        new_videos.reverse()
        for nv in new_videos:
            video = vd.download_photo_video(nv)
            if(video):
                with open(video, 'rb') as v:
                    await bot.send_video('<chat id>', v)
				
            vd.update_lastkey(nv)

async def scheduler():
    aioschedule.every().day.at("12:00").do(process_post)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)