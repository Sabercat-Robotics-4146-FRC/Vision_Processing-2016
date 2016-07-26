import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import log
__version__ = "0.0.01"
__description__ = """
The Tracker class provides a streamlined method of working with object tracking
Written by GowanR
"""

# returns True if the argument is not whitespace, False if it is
def not_whitespace( x ):
    if x != " " and x != "" and x != "\n":
        return True
    else:
        return False
# Does nothing ... or does it?
def nothing( x ):
    pass


class Tracker:
    # Constructor for tracker
    def __init__( self, capture, log, interactive=False, hsv=False, original=True, in_file=(False, ""), out_file=(False,""), display=True ):
        self.track = False
        # Pass the log object
        self.log = log
        log.info("initializing saber_track Tracker")
        # If in interactive mode, initialize HSV trackbars
        if interactive:
            self.init_trackbar()
            self.set_limits_trackbar()
        # Display determines weather to display windows
        self.display = display
        # Deal with inputs and outputs
        if in_file[0]: # If input True,
            self.set_input( in_file[1] ) # Load HSV values from .track file, apply them
            self.track = True
        if out_file[0]: # If output True,
            self.log.info("Using output file.")
            self.log.warn("Will not save unless you add *.write_on_exit() to quit!")
            self.out_file = out_file[1] # set the file that will be written on save
        # Localize the caputure object
        self.capture = capture
        # Deal with state preferances
        self.original = original
        log.info("using original: " + str(original))
        self.interactive = interactive
        log.info("using interactive: " + str(interactive))
        self.hsv = hsv
        log.info("using hsv: " + str(hsv))
    # Initialize trackbar
    def init_trackbar( self ):
        self.log.init("initializing trackbars")
        cv2.namedWindow('sliders')
        cv2.createTrackbar('H_Max','sliders',0,255,nothing)
        cv2.createTrackbar('H_Min','sliders',0,255,nothing)
        cv2.createTrackbar('S_Max','sliders',0,255,nothing)
        cv2.createTrackbar('S_Min','sliders',0,255,nothing)
        cv2.createTrackbar('V_Max','sliders',0,255,nothing)
        cv2.createTrackbar('V_Min','sliders',0,255,nothing)
        self.track = True
    # Track an explict colorspace
    def track_color( lower, upper ):
        self.upper = upper
        self.lower = lower
        self.track = True
    # Loads input file, sets upper and lower to the provided values
    def set_input( self, name ):
        self.log.init( "Writing trackfile: " + name + ".track" )
        fs = open( name + ".track", "r" )
        file = []
        for line in fs:
            file.append(line)
        self.lower = np.array(map( lambda x: int(x), filter(lambda x: not_whitespace(x),file[0].split(" ")) ))
        self.upper = np.array(map( lambda x: int(x), filter(lambda x: not_whitespace(x),file[1].split(" ")) ))
        fs.close()
        self.set_upper_trackbar( self.upper )
        self.set_lower_trackbar( self.lower )
    # Saves the HSV values to the provided out_file if it exists
    def save( self ):
        try:
            assert(self.out_file) # See if the out_file exists, if so,
            self.log.destroy("Safe exit and saveing trackfile: " + str(self.out_file) + ".track")
            file = open( str(self.out_file) + ".track", "w+") # Open out_file
            file.write( str(self.lower)[1:len(str(self.lower))-1] + " \n" ) # Write lower HSV bound
            file.write( str(self.upper)[1:len(str(self.upper))-1] + " \n" ) # Write upper HSV bound
            file.close() # Close the out_file
        except (RuntimeError, TypeError, NameError, AttributeError):
            self.log.destroy("Exiting saber_track, nothing to save")
    # Sets the upper trackbar values. Usage: value = [ h, s, v ]
    def set_upper_trackbar( self, value ):
        cv2.setTrackbarPos('H_Max','sliders',value[0])
        cv2.setTrackbarPos('S_Max','sliders',value[1])
        cv2.setTrackbarPos('V_Max','sliders',value[2])
    # Sets the lower trackbar values. Usage: value = [ h, s, v ]
    def set_lower_trackbar( self, value ):
        cv2.setTrackbarPos('H_Min','sliders',value[0])
        cv2.setTrackbarPos('S_Min','sliders',value[1])
        cv2.setTrackbarPos('V_Min','sliders',value[2])
    # Gets the values of the upper HSV values from the trackbar, returns [ h, s, v ]
    def get_upper_trackbar( self ):
        hh = cv2.getTrackbarPos('H_Max','sliders')
        sh = cv2.getTrackbarPos('S_Max','sliders')
        vh = cv2.getTrackbarPos('V_Max','sliders')
        return [ hh, sh, vh ]
    # Gets the value of the upper HSV values from the trackbar, returns [ h, s, v ]
    def get_lower_trackbar( self ):
        hl = cv2.getTrackbarPos('H_Min','sliders')
        sl = cv2.getTrackbarPos('S_Min','sliders')
        vl = cv2.getTrackbarPos('V_Min','sliders')
        return [ hl, sl, vl ]
    # Sets upper and lower values to their coresponding trackbar
    def set_limits_trackbar( self ):
        self.upper = np.array(self.get_upper_trackbar())
        self.lower = np.array(self.get_lower_trackbar())
    # Only shows windows when display is set to True
    def show( self, win_name, value ):
        if self.display:
            cv2.imshow( win_name, value )
    # Update function should be invoked whenever the camera frame needs refreshing
    def update ( self ):
        cap = self.capture.read( ) # Capture the frame from the webcam
        if self.hsv or self.track: # Convert color space to HSV if any options need it
            hsv = cv2.cvtColor( cap, cv2.COLOR_BGR2HSV )
        # Render needed video outputs
        if self.original:
            self.show( 'original', cap )
        if self.hsv:
            self.show( 'hsv', hsv)
        if self.track:
            msk = cv2.inRange( hsv, self.lower, self.upper)
            # Make images smooth again!
            msk =  cv2.blur(msk,(5,5))
            msk = cv2.erode(msk, None, iterations=2)
            msk = cv2.dilate(msk, None, iterations=2)
            self.show( 'masked', msk )
            cnts = cv2.findContours (msk.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )[-2]
            cv2.drawContours(msk, cnts, -1, (0,255,0), 3)
            #hull = cv2.convexHull(cnts)
            if len(cnts) > 0:
                pass
                #self.log.debug(str(len(cnts)))
                #x,y,w,h = cv2.boundingRect(cnts[0])
                #cv2.rectangle(msk,(x,y),(x+w,y+h),(0,255,0),2)
            self.show( 'contours', msk )

        if self.interactive:
            # Get the hsv maxes and mins
            self.set_limits_trackbar()
