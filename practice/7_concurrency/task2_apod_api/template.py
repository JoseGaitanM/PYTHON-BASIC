import aiohttp
import asyncio
import time
import os 
from aiofile import async_open
import requests

API_KEY = 'mBUKdrhIVLJu2AUXVOuRzlesWqAgA40fWZhdogr8'
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'

async def create_file(name,content):
    async with async_open(name, 'wb') as file:
        await file.write(content)

async def download_image(session,m):
    async with session.get(m['url']) as resp:
        content= await resp.read()

    name=f"output/{m['date']}.jpg"
    await create_file(name,content)


async def download_apod_images(metadata):
    async with aiohttp.ClientSession() as session:
        tasks=[]
        for m in metadata:
            if m['media_type'] == 'image':
                task = asyncio.ensure_future(download_image(session,m))
                tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)



if __name__ == '__main__':
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    start_time = time.time()

    start_date='2021-08-01'
    end_date='2021-09-30'
    url = 'https://api.nasa.gov/planetary/apod?api_key={}&start_date={}&end_date={}'.format(API_KEY,start_date,end_date)
    resp=requests.get(url)
    result=resp.json()

    asyncio.run(download_apod_images(result))

    duration = time.time() - start_time
    print('Time: ',duration)
