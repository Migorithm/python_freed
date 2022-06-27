from sys import maxsize
from fastapi import FastAPI, UploadFile, File,Form,Body, Depends

from pydantic import BaseModel, UUID4
import asyncio
import uvicorn
import cv2
import numpy as np
import base64
import io
import PIL
from PIL import Image


class User(BaseModel):
    name: str 
    age:int

    @classmethod
    def as_form(
        cls,
        name:str = Form(...),
        age: int = Form(...)
    ) -> 'User':
        return cls(name=name,age=age)


app = FastAPI()


@app.post('/')
async def upload_file(
    files: list[UploadFile] | None ,
    user :User = Depends(User.as_form) 
) -> User:
    tasks = [asyncio.create_task(file.read()) for file in files]
    images = []
    for task in asyncio.as_completed(tasks):
        file = await task
        print("--------------------------------")
        print("--------------------------------")
        print("original size:",len(file)) #Same as len, accurate size in byte

        nparr = np.fromstring(file, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) #Can't use imread as it's image object as opposed to str
        print('Original Dimensions : ',img.shape)
        
        print("size measured after cv2 : ",img.shape[1]*img.shape[0]*img.shape[2])
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        _, encoded_img = cv2.imencode('.PNG', resized)
        encoded_img = base64.b64encode(encoded_img)
    
        print('Resized Dimensions : ',resized.shape)
    
        print(resized.size)
        images.append(encoded_img)
    return user,images

@app.get('/get')
async def getter(
    user: User
) -> User:
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)