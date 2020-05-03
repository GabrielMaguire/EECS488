from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import os
import time
import imutils
import cv2
import numpy as np

############################ INITIALIZATIONS ############################
# Load haar cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
upper_body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

# Preset frame dimensions
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

# Video encoding
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID')
}

# Save captured images for website to access
images_dir = "/var/www/html/images"
video_dir = "videos/"

# Initialize camera
cap = cv2.VideoCapture(0)


def main():
    
    recorder = None
    
    frame_count = 0
    movtext = "N/A"
    rectext = "OFF"
    approach = False
    
    target = []
    track_target = []
    avg_target = []
    tolerance = 30
    extra_frames = 10
    approach_count = 0

    while (True):
        
        start_time = time.time()
        frame_count = frame_count + 1       # increment counter per frame
        ret, image = cap.read()
        # ~ out.write(image)
        
        text = "Unoccupied"
        
        # Add the current frame to the video if recording is set
        if recorder:
            recorder.write(image)
            rectext = "ON"
            if not approach:
                extra_frames = extra_frames - 1
                if (extra_frames < 0):
                    recorder = None
                    extra_frames = 10
                
        else:
            rectext = "OFF"
        
        # resize the frame, convert it to grayscale
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        
        '''
        The following code implements haar cascades to attempt to draw a rectangle around all bodies
        found, and all faces found inside the area of the bodies.
        '''
        ################## HAAR CASCADE CALCULATION ####################
        bodies = upper_body_cascade.detectMultiScale(gray, 1.2, 7)
        for (x, y, w, h) in bodies:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            text = "Occupied"
            height = h
            if not target:
                if (w > 65 and h > 50):
                    target = [x, y, w, h]
                    print("Target initialized")
            elif (x < target[0] + tolerance and x > target[0] - tolerance and y < target[1] + tolerance and y > target[1] - tolerance and w > 65 and h > 50):
                target = [x, y, w, h]
                track_target.append(h)
                if (len(track_target) >= 5):
                    average_height = sum(track_target) / len(track_target)
                    avg_target.append(average_height)
                    track_target = []
                    print(avg_target[-1])
                    if (len(avg_target) > 2):
                        if (avg_target[-1] > 3 + avg_target[-2]):
                            approach_count = approach_count + 1
                            approach = True
                            movtext = "APPROACHING"
                            print("APPROACHING")
                            if (approach_count == 2):
                                image_name = datetime.now().strftime("%Y%b%d_%H:%M:%S") + ".jpg"
                                cv2.imwrite(os.path.join(images_dir, image_name), image)
                            if (approach_count > 2 and not recorder):
                                vid_name = os.path.join(video_dir, datetime.now().strftime("Rec_%Y%b%d_%H.%M.%S") + ".avi")
                                recorder = cv2.VideoWriter(vid_name, VIDEO_TYPE['avi'], 7, STD_DIMENSIONS["480p"])
                        else:
                            approach_count = 0
                            approach = False
                            movtext = "NOT APPROACHING"
                            print("NOT APPROACHING")
                                
            else:
                print("---")
                
        
        
        
        
        
        # Display the video feed with additions of body detection
        # ~ cv2.putText(image, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, "Subject Movement: {}".format(movtext), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # ~ cv2.putText(image, "Recording: {}".format(rectext), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('Video Feed',image)    # title of the window
        
        
        ################### KEYBOARD INPUT HANDLING ####################
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break
            
        elif key == ord("s"):
            print("SAVING IMAGE")
            image_name = datetime.now().strftime("%Y%b%d_%H:%M:%S") + ".jpg"
            cv2.imwrite(os.path.join(images_dir, image_name), image)
            
        elif key == ord("v"):
            vid_name = os.path.join(video_dir, datetime.now().strftime("Rec_%Y%b%d_%H:%M:%S") + ".avi")
            recorder = cv2.VideoWriter(vid_name, VIDEO_TYPE['avi'], 7, STD_DIMENSIONS["480p"])
            rec_flag = True      # video write
            print("START RECORDING: " + vid_name)
            
        elif key == ord("c"):
            recorder = None
            print("STOP RECORDING")
            
        
        
        # Calculate total frame processing time
        end_time = time.time()
        delta_time = round(end_time - start_time, 3)
        # ~ print(delta_time)
        
    
    if recorder:
        recorder.release()
    cap.release()
    

main()
cv2.destroyAllWindows()
