import cv2
import os
dirname = os.path.dirname(os.path.abspath(__file__))
print(dirname)
img_file = dirname + "/pic1.png"
save_file = dirname + "/modified_pic1.png"
img = cv2.imread(img_file,cv2.IMREAD_GRAYSCALE) # numpy.ndarray

if img is not None:
    cv2.imshow("IMG",img) # display images
    cv2.imwrite(save_file,img) #save image 
    cv2.waitKey() #Wait until  key is inserted, if it were not for this, the image will be shut down immediately after showing one.
    cv2.destroyAllWindows() # close the all the windows