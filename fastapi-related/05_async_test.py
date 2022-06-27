import asyncio
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def async_test(num:int):
    lst = [ value async for value in some_async_func(num)]
    return lst

async def task(num):
    await asyncio.sleep(5) #alternative to I/O bound call
    return f"message {num}"


async def some_async_func(num,ah=None):
    tasks = [task(_) for _ in range(num)]
    for value in asyncio.as_completed(tasks):
        yield await value
    
def upload_to_bucket(file_obj):
    return some_async_func(5,"ahaha")


if __name__ == "__main__":
    uvicorn.run(app,port=8001)