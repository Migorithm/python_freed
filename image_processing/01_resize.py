import cv2
import os

dirname = os.path.abspath(os.path.dirname(__file__))


img = cv2.imread(dirname + "/tower.png",cv2.IMREAD_UNCHANGED)
print('Original Dimensions : ',img.shape)
print(img.size)

scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
print(resized.size)
 
cv2.imshow("Resized image", resized)
