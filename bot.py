import asyncio
import aioschedule
import logging

from aiogram import Dispatcher, Bot, executor, types

from media import VideoDownloader

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = '<BOT TOKEN>'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

vd = VideoDownloader("lastkey.txt")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm MediaBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def process_post():
    new_videos = vd.new_videos()

    if(new_videos):
        new_videos.reverse()
        for nv in new_videos:
            if(vd.download_photo_video(nv)):
                with open(vd.download_photo_video(nv), 'rb') as video:
                    await bot.send_video('<bot id>', video)
                print('video sent')
            else:
                print('it was photo')
				
            vd.update_lastkey(nv)

async def scheduler():
    aioschedule.every().day.at("10:39").do(process_post)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)