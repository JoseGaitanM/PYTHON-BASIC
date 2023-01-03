import os
from random import randint
import time
import sys
import multiprocessing
import csv
import asyncio
import aiofiles
from aiocsv import AsyncWriter,AsyncReader

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'
sys.set_int_max_str_digits(500000)

def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""
    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    file = 'output/'+str(n)+'.txt'
    with open(file, 'w+') as f:
        f.write(str(f1))

def func0(array):
    for n in array:
        fib(n)

def func1(array):
    with multiprocessing.Pool() as pool:
        pool.map(fib, array)

def func2(result_file: str,callable:list):
    f = open(result_file, 'w+', encoding='UTF8')
    writer = csv.writer(f)
    for i in callable:
        with open(f'output/{i}.txt') as f:
            contents = int(f.read())
            writer.writerow([str(i),str(contents)])

async def func2_asyncio(result_file: str,callable:list):
    async with aiofiles.open(result_file, 'w+', encoding='UTF8') as fr:
            writer = AsyncWriter(fr)
            for i in callable:
                async with aiofiles.open(f'output/{i}.txt') as f:
                    contents = int(await f.read())
                    await writer.writerow([str(i),str(contents)])

if __name__ == '__main__':
    print("User Current Version:-", sys.version)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    array=[randint(1000, 100000) for _ in range(1000)]

    start_time = time.time()
    func0(array)
    duration = time.time() - start_time
    print('Normal time: ',duration)

    start_time = time.time()
    func1(array)
    duration = time.time() - start_time
    print('Multiprocessing time: ',duration)

    start_time = time.time()
    func2(RESULT_FILE,array)
    duration = time.time() - start_time
    print('Normal time result file: ',duration)

    start_time = time.time()
    asyncio.run(func2_asyncio(RESULT_FILE,array))
    duration = time.time() - start_time
    print('Time asyncio result file: ',duration)