import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
import uvicorn
from operator import mul
app = FastAPI()

def prepare(image):
    IMG_SIZE = 224
    new_array = cv2.resize(image, (IMG_SIZE, IMG_SIZE)) 
    return new_array.reshape(-1, IMG_SIZE,IMG_SIZE,3)


@app.post("/")
async def root(file: UploadFile = File(...)):
    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height,width,channel = img.shape[:3]
    print(height*width*channel)
    #resize
    dst1 = cv2.resize(img, (int(width*0.5),int(height*0.5)),\
                     interpolation=cv2.INTER_AREA)
                     
    print(dst1.shape[0]*dst1.shape[1]*dst1.shape[2])

    cv2.imshow("small",dst1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return 2



if __name__ == "__main__":
    uvicorn.run("image_upload:app",reload=True)