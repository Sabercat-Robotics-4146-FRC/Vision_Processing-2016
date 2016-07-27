import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import log
from networktables import NetworkTable
import logging
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
    def __init__( self, capture, log, port="",filters="",interactive=False, hsv=False, original=True, in_file="", out_file="", display=True ):
        self.track = False
        # Pass the log object
        self.log = log
        log.init("initializing saber_track Tracker")
        # If the port tag is True, set the
        if port != "":
            NetworkTable.setIPAddress(ip)
            NetworkTable.setClientMode()
            NetworkTable.initialize()
            self.smt_dash = NetworkTable.getTable("SmartDashboard")
        # If in interactive mode, initialize HSV trackbars
        if interactive:
            if in_file == "":
                if filters != "":
                    filters = filters.split(" ")
                    self.limits = {}
                    for i in filters:
                        self.limits[i] = [ [0,0,0], [0,0,0] ]
                    for w, _ in self.limits.items():
                        self.init_trackbar( w )
                    self.set_limits_trackbar( self.limits )
        # Display determines weather to display windows
        self.display = display
        # Deal with inputs and outputs
        if in_file != "": # If input is not default,
            self.set_input( in_file ) # Load HSV values from .track file, apply them
            self.track = True
        if out_file != "": # If output True,
            self.log.info("Using output file.")
            self.log.warn("Will not save unless you add *.write_on_exit() to quit!")
            self.out_file = out_file # set the file that will be written on saved
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
    def init_trackbar( self, window ):
        self.log.init("initializing trackbars" + str(window) )
        cv2.namedWindow( window )
        cv2.createTrackbar('H_Max',window,0,255,nothing)
        cv2.createTrackbar('H_Min',window,0,255,nothing)
        cv2.createTrackbar('S_Max',window,0,255,nothing)
        cv2.createTrackbar('S_Min',window,0,255,nothing)
        cv2.createTrackbar('V_Max',window,0,255,nothing)
        cv2.createTrackbar('V_Min',window,0,255,nothing)
        self.track = True
    # Track an explict colorspace
    def track_color( lower, upper ):
        self.upper = upper
        self.lower = lower
        self.track = True
    # Loads input file, sets upper and lower to the provided values
    def set_input( self, name ):
        self.limits = {}
        self.log.init( "Reading trackfile: " + name + ".track" )
        fs = open( name + ".track", "r" )
        in_file = []
        for line in fs:
            in_file.append( line )
        for i in range(len(in_file)):
            if i % 3 == 0:
                l = np.array(map( lambda x: int(x), filter(lambda x: not_whitespace(x),in_file[i+1].split(" ")) ))
                u = np.array(map( lambda x: int(x), filter(lambda x: not_whitespace(x),in_file[i+2].split(" ")) ))
                self.limits[in_file[i]] = [ l, u ]
        fs.close()
        for k, v in self.limits.items():
            self.init_trackbar( k )
            self.set_upper_trackbar( v[0], k )
            self.set_lower_trackbar( v[1], k )
    def update_table( self, value_dict ):
        for k, v in value_dict.items(): # for each value in the dictionary,
            smt_dash.putNumber( k, v ) # put the values of the dictionarys on the networktable
        pass
    # Saves the HSV values to the provided out_file if it exists
    def save( self ):
        try:
            assert(self.out_file) # See if the out_file exists, if so,
            self.log.destroy("Safe exit and saveing trackfile: " + str(self.out_file) + ".track")
            file = open( str(self.out_file) + ".track", "w+") # Open out_file
            for k, v in self.limits.items():
                file.write( k )
                file.write( str(v[0])[1:len(str(v[0]))-1] + " \n")
                file.write( str(v[1])[1:len(str(v[1]))-1] + " \n")
            file.close() # Close the out_file
        except (RuntimeError, TypeError, NameError, AttributeError):
            self.log.destroy("Exiting saber_track, nothing to save")
    # Sets the upper trackbar values. Usage: value = [ h, s, v ]
    def set_upper_trackbar( self, value, window ):
        cv2.setTrackbarPos('H_Max',window,value[0])
        cv2.setTrackbarPos('S_Max',window,value[1])
        cv2.setTrackbarPos('V_Max',window,value[2])
    # Sets the lower trackbar values. Usage: value = [ h, s, v ]
    def set_lower_trackbar( self, value, window ):
        cv2.setTrackbarPos('H_Min',window,value[0])
        cv2.setTrackbarPos('S_Min',window,value[1])
        cv2.setTrackbarPos('V_Min',window,value[2])
    # Gets the values of the upper HSV values from the trackbar, returns [ h, s, v ]
    def get_upper_trackbar( self, window ):
        hh = cv2.getTrackbarPos('H_Max',window)
        sh = cv2.getTrackbarPos('S_Max',window)
        vh = cv2.getTrackbarPos('V_Max',window)
        return [ hh, sh, vh ]
    # Gets the value of the upper HSV values from the trackbar, returns [ h, s, v ]
    def get_lower_trackbar( self, window ):
        hl = cv2.getTrackbarPos('H_Min',window)
        sl = cv2.getTrackbarPos('S_Min',window)
        vl = cv2.getTrackbarPos('V_Min',window)
        return [ hl, sl, vl ]
    # Sets upper and lower values to their coresponding trackbar
    def set_limits_trackbar( self, value ):
        for k, v in value.items():
            v[0] = np.array(self.get_upper_trackbar( k ))
            v[1] = np.array(self.get_lower_trackbar( k ))
    # Only shows windows when display is set to True
    def show( self, win_name, value ):
        if self.display:
            cv2.imshow( win_name, value )
    def get_bounding_rect( self, cap, hsv, win ):
        lower = self.get_lower_trackbar( win )
        upper = self.get_upper_trackbar( win )
        msk = cv2.inRange( hsv, np.array(lower), np.array(upper))
        # Make images smooth again!
        msk =  cv2.blur(msk,(5,5))
        msk = cv2.erode(msk, None, iterations=3)
        msk = cv2.dilate(msk, None, iterations=3)
        if self.interactive:
            self.show( str(win)+ " Image", msk )
        im2, contours, hierarchy = cv2.findContours( msk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
        if len(contours) > 0:
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnts = contours[max_index]
            cv2.drawContours(msk, [cnts], 0, (0,255,0), 3)
            x,y,w,h = cv2.boundingRect(cnts)
            cv2.rectangle(cap,(x,y),(x+w,y+h),(255,255,255),2)
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
            for k, v in self.limits.items():
                self.get_bounding_rect( cap, hsv, k )
