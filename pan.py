import numpy as np
import cv2
import os

if os.path.exists("pan"):
    os.chdir("pan")
    path=os.getcwd()
else:
    os.mkdir("pan")
    os.chdir("pan")
    path=os.getcwd()

cam = cv2.VideoCapture(0)
i=0
while True:
    ret, frame = cam.read()
    cv2.imshow('f', frame)
    key = cv2.waitKey(1)
    if key==ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
    elif key==ord('s'):
        img_name ="f_{}.png".format(i)
        p=os.path.join(path, img_name)
        cv2.imwrite(p,frame)
        inew=cv2.imread(p)
        inew=cv2.imshow(img_name, inew)
        cv2.waitKey(1000)
        i+=1
        
im=[]
mylist=os.listdir(path)
for x in mylist:
    img=cv2.imread(f'{path}/{x}')
    cimg=cv2.resize(img,(0,0),None,0.7,0.7)
    im.append(cimg)

s=cv2.Stitcher.create()
(status, result)=s.stitch(im)
if (status==cv2.STITCHER_OK):
    pn=path+'/'+'panorama'
    os.mkdir(pn)
    cv2.imwrite(pn+'/'+'pan.png', result)
    print('Your Panorama is ok')
    pan=cv2.imread(pn+'/'+'pan.png')
    pan=cv2.imshow("pan", pan)
    cv2.waitKey(0)
else:
    print('Your Panorama not! \nERR_NEED_MORE_IMGS = 1: \nERR_HOMOGRAPHY_EST_FAIL = 2 \nERR_CAMERA_PARAMS_ADJUST_FAIL = 3 \n', status)
    
cam.release()
cv2.destroyAllWindows()
