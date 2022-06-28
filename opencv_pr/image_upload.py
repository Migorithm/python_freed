import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
import uvicorn
import asyncio

app = FastAPI()

async def prepare(image_files:list[UploadFile]):
    tasks = [asyncio.create_task(image.read()) for image in image_files]
    contents = await asyncio.gather(*tasks)
    img_list = []
    for content in contents:
        nparr = np.frombuffer(content,np.uint8)
        img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        height,width,channel = img.shape[:3]
        
        #resize
        while height * width * channel > 1024 * 1024 * 2:
            height *= 0.9
            width *= 0.9
        resized_img = cv2.resize(
                            img, 
                            (int(width),int(height)),
                            interpolation=cv2.INTER_AREA
                                )
        print(height*width*channel)
        img_list.append(resized_img)
    return img_list              


@app.post("/")
async def root(files: list[UploadFile] = File(...)):
    resized_imgs = await prepare(files)
 
    for i in resized_imgs:
        cv2.imshow("small",i)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    return 2



if __name__ == "__main__":
    uvicorn.run("image_upload:app",reload=True)