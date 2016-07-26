import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import log

__description__ = """
The Tracker class provides a streamlined method of working with object tracking
Written by GowanR
"""
def nothing( x ):
    pass
# Initialize trackbar
def init_trackbar( log ):
    log.init("initializing trackbars")
    cv2.namedWindow('sliders')
    cv2.createTrackbar('H_Max','sliders',0,255,nothing)
    cv2.createTrackbar('H_Min','sliders',0,255,nothing)
    cv2.createTrackbar('S_Max','sliders',0,255,nothing)
    cv2.createTrackbar('S_Min','sliders',0,255,nothing)
    cv2.createTrackbar('V_Max','sliders',0,255,nothing)
    cv2.createTrackbar('V_Min','sliders',0,255,nothing)
class Tracker:
    def __init__( self, capture, log, interactive=False, hsv=False, original=True ):
        self.log = log
        log.info("initializing saber_track Tracker")
        self.capture = capture
        self.original = original
        log.info("using original: " + str(original))
        self.interactive = interactive
        log.info("using interactive: " + str(interactive))
        self.hsv = hsv
        log.info("using hsv: " + str(hsv))
        self.track = False
        if self.interactive:
            init_trackbar( self.log )
            self.track_color([0,0,0], 10)
    def track_color( self, value, tolerance ):
        self.log.info("tracking color: " + str(value) )
        self.tolerance = tolerance
        self.track = True
        self.track_value = np.array(value)
        self.upper = np.array(map(lambda x: x + self.tolerance, value))
        self.lower = np.array(map(lambda x: x - self.tolerance, value))
    def update ( self ):
        cap = self.capture.read( ) # Capture the frame from the webcam
        if self.hsv or self.track: # Convert color space to hsv if any options need it
            hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
        # Render needed video outputs
        if self.original:
            cv2.imshow( 'original', cap )
        if self.hsv:
            cv2.imshow( 'hsv', hsv)
        if self.track:
            cv2.imshow( 'filtered', cv2.inRange( hsv, self.lower, self.upper) )
        if self.interactive:
            # Get the hsv maxes and mins
            hh = cv2.getTrackbarPos('H_Max','sliders')
            hl = cv2.getTrackbarPos('H_Min','sliders')
            sh = cv2.getTrackbarPos('S_Max','sliders')
            sl = cv2.getTrackbarPos('S_Min','sliders')
            vh = cv2.getTrackbarPos('V_Max','sliders')
            vl = cv2.getTrackbarPos('V_Min','sliders')
            self.upper = np.array([hh,sh,vh])
            self.lower = np.array([hl,sl,vl])
