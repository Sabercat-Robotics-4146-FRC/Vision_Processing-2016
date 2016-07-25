import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import argparse
from log import Log
from saber_track import Tracker
import argparse

# Parse some command line arguments!
parser = argparse.ArgumentParser(description='HSV color sliders for video.')
parser.add_argument('--vidmode', dest='vidmode', type=int, help='video_mode = 0 for webcam', default=0)
args = parser.parse_args()

log = Log("debug_log")
vs = WebcamVideoStream(src=args.vidmode).start() # Initialize the camera object on a seperate I/O thread
st = Tracker( vs, log, hsv=True, interactive=True )
st.track_color([49,255,255], 10)
while True:
    st.update()
    # Quit with the "q" key!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        log.kill("User Invoked Safe Quit")
        break
cv2.destroyAllWindows()
vs.stop()
