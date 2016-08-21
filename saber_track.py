import cv2
from imutils.video import WebcamVideoStream
import imutils
import json
import numpy as np
import log
from networktables import NetworkTable
import logging
import time
__version__ = "0.0.3"
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

    # Constructor. Usage object_name = Tracker( cap, log )
    # handles all of the options for Construction

    def __init__( self, capture, log, port="",filters="", hsv=False, original=True, in_file="", out_file="", display=True ):
        self.limits = {}
        # Pass the log object
        self.log = log
        log.init( "initializing saber_track Tracker" )

        # If the port tag is True, set the
        if port != "":
            logging.basicConfig( level=logging.DEBUG )
            NetworkTable.setIPAddress( port )
            NetworkTable.setClientMode( )
            NetworkTable.initialize( )
            self.smt_dash = NetworkTable.getTable( "SmartDashboard" )

        # initialize the filters. If the filter is the default: "", it will not create trackbars for it.
        self.init_filters( filters )

        # Deal with filters
        self.display = display # If this is True, It will be in a windowless mode.

        # Deal with inputs and outputs
        self.out_file = str( out_file ) # set the file that will be written on saved
        self.set_input( str(in_file) ) # Load HSV values from .json file, apply them
        # Localize the caputure object
        self.capture = capture
        # Deal with state preferances
        self.original = original # if True, this will make a raw image with the trackerbox visible
        log.info("using original: " + str(original) )
        self.hsv = hsv # if True, it will display a window with the hsv colorspace displayed
        log.info( "using hsv: " + str(hsv) )
        # if there are any color limits (Upper and Lower hsv values to track) make the tracking code runs
        if len( self.limits ) > 0:
            self.track = True
        else:
            self.track = False
        self.log.info( "Tracking: " + str(self.track) )

    # The self.init_filters( filters ) function will take a string of filters and break it up by spaces
    # Each whitespace isolated string will become the name of a limit and trackbar.
    # Example, the self.init_filters( "hello world") would split the string into two windows, "hello" and "world"
    # The windows will be trackbars and will get their own tracking bounding box, tag, and binary color window

    def init_filters( self, filters ):
        if filters != "": # if there are actually filters given,
            filters = filters.split(" ") # split the filters by spaces, "red blue" => [ "red", "blue" ]
            self.filters = filters # set the global filters
            for i in filters: # cycle throught the filters
                self.init_trackbar( i ) # initializing a trackbar for each filter
                self.limits[ i ] = [ self.get_upper_trackbar( i ) , self.get_lower_trackbar( i ) ] # add a limit trackbar values
            self.interactive = True # make the session interactive
        else:
            self.filters = [] # make filters empty when no filters given
            self.interactive = False # if no filters were given, the session is not interactive

    # Initialize trackbar with window name
    # Usage: self.init_trackbar( "window_name" )
    # will make a window with the given name and initialize trackbars that
    # represent the HSV minimum and maximum values to filter

    def init_trackbar( self, window ): #
        self.log.init("initializing trackbars " + str(window) )
        cv2.namedWindow( window )
        cv2.createTrackbar('H_Max',window,0,255,nothing)
        cv2.createTrackbar('H_Min',window,0,255,nothing)
        cv2.createTrackbar('S_Max',window,0,255,nothing)
        cv2.createTrackbar('S_Min',window,0,255,nothing)
        cv2.createTrackbar('V_Max',window,0,255,nothing)
        cv2.createTrackbar('V_Min',window,0,255,nothing)

    # Loads input file, sets upper and lower to the provided values
    # Usage: self.set_input( "in_file_name" )
    # !! Can only load the *.json files !! ( you may also write .json files yourself )

    def set_input( self, name ):
        if name == "": # if no file is given, stop the function
            return
        self.log.init( "Reading trackfile: " + name + ".json" )
        fs = open( name + ".json", "r" ) # open the file under a .json extention
        data = json.loads( fs.read() )
        self.limits.update( data )
        fs.close( ) # close the file

    # Updates a dictionary to the networktable
    # Usage: self.update_table( { "key" : value } )
    # will make a networktable: | key | value |

    def update_table( self, value_dict ):
        for k, v in value_dict.items(): # for each value in the dictionary,
            smt_dash.putNumber( k, v ) # put the values of the dictionarys on the networktable
        pass

    # Saves the HSV values to the provided out_file if it exists
    # The HSV values are stored in self.limits
    # Usage: self.save( )

    def save( self ):
        if self.out_file == "": # If the out_file is not given, dont save anything
            self.log.destroy("Exiting saber_track, nothing to save")
        else: # if an out_file was given,
            jfile = open( self.out_file + ".json", "w+" )
            jfile.write( str ( json.dumps (self.limits) ) )
            jfile.close() # Close the out_file
            self.log.info( "Wrote to file " + str(self.out_file) + ".json success." )

    # Sets the upper trackbar values.
    # Usage: self.set_upper_trackbar( [ h, s, v ], "window_name")
    # sets the trackbar's values to the given value

    def set_upper_trackbar( self, value, window ):
        cv2.setTrackbarPos('H_Max',window,value[0])
        cv2.setTrackbarPos('S_Max',window,value[1])
        cv2.setTrackbarPos('V_Max',window,value[2])

    # Sets the lower trackbar values.
    # Usage: self.set_lower_trackbar( [ h, s, v ], "window_name" )
    # Sets the lower trackbar values to the given values

    def set_lower_trackbar( self, value, window ):
        cv2.setTrackbarPos('H_Min',window,value[0])
        cv2.setTrackbarPos('S_Min',window,value[1])
        cv2.setTrackbarPos('V_Min',window,value[2])

    # Gets the values of the upper HSV values from the trackbar
    # Usage: self.get_upper_trackbar( "window_name" )
    # Returns a numpy array: ap.array( [ h, s, v ] )

    def get_upper_trackbar( self, window ):
        hh = cv2.getTrackbarPos('H_Max',window)
        sh = cv2.getTrackbarPos('S_Max',window)
        vh = cv2.getTrackbarPos('V_Max',window)
        return [ hh, sh, vh ]

    # Gets the value of the lower HSV values from the trackbar
    # Usage: self.get_lower_trackbar( "window_name" )
    # Returns numpy array: np.array( [ h, s, v ] )

    def get_lower_trackbar( self, window ):
        hl = cv2.getTrackbarPos('H_Min',window)
        sl = cv2.getTrackbarPos('S_Min',window)
        vl = cv2.getTrackbarPos('V_Min',window)
        return [ hl, sl, vl ]

    # Sets upper and lower values to their coresponding trackbar
    # Usage: self.set_limits_trackbar( { "window_name": [ np.array([h,s,v]), np.array([h,s,v]) ] } )
    # set the value to their corresponding trackbar if the key is to be filtered

    def set_limits_trackbar( self, value ):
        for k, v in value.items( ):
            if k in self.filters:
                v[0] = self.get_upper_trackbar( k )
                v[1] = self.get_lower_trackbar( k )

    # Only shows windows when display is set to True
    # Usage: self.show( "window_name", image_matrix )

    def show( self, win_name, value ):
        if self.display:
            cv2.imshow( win_name, value )

    # Gets the largest bounding box by area of a colorspace within the upper and lower values
    # with respect to the capture
    # Usage: self.get_bounding_rect( capture_to_analyse, capture_to_show, "window_name", np.array([h,s,v]), np.array([h,s,v]) )
    # You may set the argument return_value = True if you would like the funiton to return the box values
    # TODO:
    # - Reduce noise
    # - labling

    def get_bounding_rect( self, key, cap, win_cap, win, upper, lower, return_value=False, text=True ):
        hsv = cv2.cvtColor( cap, cv2.COLOR_BGR2HSV )
        hsv = cv2.blur(hsv,(5,5)) # blur the image for smoothing
        msk = cv2.inRange( hsv, np.array(lower), np.array(upper) ) # get an object of all of the pixels with color values in the range
        # Make images smooth again!
        #msk = cv2.blur(msk,(5,5))
        msk = cv2.erode(msk, None, iterations=3) # erode the image to reduce background noise
        msk = cv2.dilate(msk, None, iterations=3) # dilate the image to reduce background noise
        if self.display: # if the display is true,
            self.show( str(win)+ " Image", msk ) # show the binary range image
        # Get the image contours in the mask
        im2, contours, hierarchy = cv2.findContours( msk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
        # If a contour was found
        if len(contours) > 0:
            areas = [cv2.contourArea(c) for c in contours] # get the area of each contour
            max_index = np.argmax(areas) # get the index of the largest contour by area
            cnts = contours[max_index] # get the largest contout by area
            cv2.drawContours(msk, [cnts], 0, (0,255,0), 3) # Draw the contours to the mask image
            x,y,w,h = cv2.boundingRect(cnts) #  get the bouding box information about the contour
            cv2.rectangle(win_cap,(x,y),(x+w,y+h),(255,255,255),2) # Draw rectangle on the image to represent the bounding box
            if self.smt_dash != None:
                self.smt_dash.putNumber('vis_x', x)
                self.smt_dash.putNumber('vis_y', y)
                self.smt_dash.putNumber('vis_w', w)
                self.smt_dash.putNumber('vis_h', h)
            if text:
                cv2.putText( win_cap , str(key), ( x, y+h ), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            if return_value: # if the function needs a return value
                return [ x, y, w, h ] # return an array of the bounding box values

    # Update function should be invoked whenever the camera frame needs refreshing
    # Usage: self.update( )
    # This should be embedded inside a while loop

    def update ( self ):
        cap = self.capture.read( ) # Capture the frame from the webcam
        show_cap = cap.copy()
        # Render needed video outputs
        if self.hsv:
            hsv = cv2.cvtColor( cap, cv2.COLOR_BGR2HSV )
            self.show( 'hsv', hsv )
        if self.track: # if the program should track an item
            for k, v in self.limits.items( ): # Cycle through each item in the limits
                if k in self.filters: # if the value is in the filters given,
                    v[0] = self.get_upper_trackbar( k ) # set the upper to the trackbar value
                    v[1] = self.get_lower_trackbar( k ) # set the lower to the trackbar value
                self.get_bounding_rect( k, cap, show_cap, k, v[0], v[1] ) # Get the bounding rect of the capture with limits
        if self.original:
            self.show( 'original', show_cap )
