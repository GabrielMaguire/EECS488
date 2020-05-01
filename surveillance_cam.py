from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import os
import time
import imutils
import cv2
import numpy as np

# Load haar cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

# Save captured images for website to access
images_dir = "/var/www/html/images"

# initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)


def main():
    
    body_pos_info = tuple()
    
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        start_time = time.time()
        
        image = frame.array
        
        # resize the frame, convert it to grayscale, and blur it
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        '''
        The following code implements haar cascades to attempt to draw a rectangle around all bodies
        found, and all faces found inside the area of the bodies.
        '''
        '''
        bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in bodies:
        print("BODY:")
        print(bodies)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        '''
        '''
        roi_gray = gray[y:h+h, x:x+w]
        roi_color = image[y:h+h, x:x+w]
        faces = face_cascade.detectMultiScale(roi_gray)
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(roi_color, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 2)
        '''
        
        
        # Display the video feed with additions of body detection
        cv2.imshow("Video Feed", image)
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        
        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            print("SAVING IMAGE")
            image_name = datetime.now().strftime("%Y%b%d_%H:%M:%S") + ".jpg"
            cv2.imwrite(os.path.join(images_dir, image_name), image)
            
        end_time = time.time()
        delta_time = round(end_time - start_time, 2)
        print(delta_time)
    

if __name__ == "__main__":
    main()
