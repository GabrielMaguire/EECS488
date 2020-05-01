import numpy as np
import os
import time
from datetime import datetime
import cv2

############################ INITIALIZATIONS ############################
dir = "C:\\Users\\Sung Yoon\\Documents\\Python\\EECS488"
vid_name = 'C:\\Users\\Sung Yoon\\Documents\\Python\\EECS488\\video.avi'
counter = 0
sus_counter = 0
height = 0
old_h = 0
movtext = "N/A"
rectext = "OFF"
rec_flag = False
ubody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# Video Encoding, might require additional installs (http://www.fourcc.org/codecs.php)
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

############################ METHODS ############################
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height

def get_video_type(vid_name):
    vid_name, ext = os.path.splitext(vid_name)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

############################ CODE ############################
cap = cv2.VideoCapture(0)   #cap = capture
out = cv2.VideoWriter(vid_name, get_video_type(vid_name), 10, get_dims(cap, "480"))

while 1:
    counter = counter + 1       # increment counter per frame
    #print(counter)
    ret, img = cap.read()       # ret = return value (T/F), img = next frame
    text = "Unoccupied"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 3)
    bodies = ubody_cascade.detectMultiScale(gray, 1.05, 3)

    ########## recording ###########
    if (rec_flag == True):
        out.write(img)
        rectext = "ON"
    else:
        rectext = "OFF"

    for (x,y,w,h) in bodies:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]       # roi = region of interest
        roi_color = img[y:y+h, x:x+w]
        text = "Occupied"
        height = h

    if (counter == 10):     # adjust number to change rate of checking
        print(height)
        if (height > old_h*1.05):
            movtext = "APPROACHING"
            sus_counter = sus_counter + 1
        else:
            movtext = "NOT APPROACHING"
        old_h = height
        counter = 0

    if (sus_counter == 3):
        vid_name = os.path.join(dir, datetime.now().strftime("Rec_%Y%b%d_%H.%M.%S") + ".avi")
        out = cv2.VideoWriter(vid_name, get_video_type(vid_name), 15, get_dims(cap, "480"))
        rec_flag = True      # video write
        sus_counter = 0

    cv2.putText(img, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(img, "Subject Movement: {}".format(movtext), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(img, "Recording: {}".format(rectext), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Video Feed',img)    # title of the window

    # user-input dependent actions
    key = cv2.waitKey(30) & 0xff    # wait 30 ms and record the pressed key
    if key == ord("q"):
        break
    elif key == ord("s"):
        print("SAVING IMAGE")
        image_name = datetime.now().strftime("%Y%b%d_%H.%M.%S") + ".jpg"
        cv2.imwrite(os.path.join(dir, image_name), img)
    # elif key == ord("v"):
    #     key = cv2.waitKey(30) & 0xff
    #     rec_flag = True      # video write
    #     vid_name = os.path.join(dir, datetime.now().strftime("Rec_%Y%b%d_%H.%M.%S") + ".avi")
    #     out = cv2.VideoWriter(vid_name, get_video_type(vid_name), 15, get_dims(cap, "480"))
    elif key == ord("c"):
        rec_flag = False

cap.release()
out.release()
cv2.destroyAllWindows()
