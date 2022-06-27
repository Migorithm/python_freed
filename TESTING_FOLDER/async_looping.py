import asyncio


async def some_async_task():
    await asyncio.sleep(1)
    return "Yes!"


async def looping_async(number:int):
    tasks = [   
            asyncio.create_task(some_async_task()) 
                for _ in range(number)
            ]
    for value in asyncio.as_completed(tasks):
        yield await value


async def main():
    async for i in looping_async(5):
        print(i)

if __name__ == "__main__":
    asyncio.run(main())