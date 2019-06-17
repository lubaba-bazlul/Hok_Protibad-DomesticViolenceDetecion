# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import imutils
import argparse
import time
import cv2
import os


# collect parameters 
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-l", "--len", type=int, default=5,
	help="length of the video in seconds")
ap.add_argument("-w", "--initWait", type=int, default=3,
	help="initial waiting time")
args = vars(ap.parse_args())

# Parameters
output = args['output']
fps = args['fps']
videoLen = args['len'] 
initalWaitTime = args['initWait']
picamera = args['picamera']
codec = args['codec']

frameCount = 0
totalFrameNo = videoLen*fps



# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=picamera > 0).start()
time.sleep(initalWaitTime)
os.system( "say go" )


# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*codec)
writer = None
(h, w) = (None, None)


# loop over frames from the video stream
while True:
    # grab the frame from the video stream and resize it to have a
    # maximum width of 300 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=300)
    frameCount = frameCount + 1

    # check if the writer is None
    if writer is None:
        # store the image dimensions, initialize the video writer,
        # and construct the zeros array
        (h, w) = frame.shape[:2]
        writer = cv2.VideoWriter(output, fourcc, fps, (w, h), True)
        
    writer.write(frame)
    # show the frames
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q") or frameCount == totalFrameNo:
        break
    
# do a bit of cleanup
print("[INFO] cleaning up...")
vs.stop()

writer.release()
cv2.destroyAllWindows()
time.sleep(1)
vs.stream.release()

