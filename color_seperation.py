import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np

cv2.namedWindow('image')
# A funciton that passes the value.
def nothing( x ):
    pass
# Define trackbars to filter color values.
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)
# constructs an BRG color value to pass to the converter
bgr = lambda b, g, r: np.uint8([[[b,g,r ]]])
# Converts an BGR to HSV color space
convert_hsv = lambda x: np.array(cv2.cvtColor( x, cv2.COLOR_BGR2HSV )[0][0])
# Thread that shit!
vs = WebcamVideoStream(src=1).start() # Initialize the camera object on a seperate I/O thread
# define range of blue color in HSV
lower = convert_hsv( bgr(149, 255, 255 ) )
upper = convert_hsv( bgr( 66, 122, 141) )
while True:
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    lower = convert_hsv( bgr( b-20,g-20,r-20 ) )
    upper = convert_hsv( bgr( b+20,g+20,r+20 ) )
    frame = vs.read( ) # Read frome from camera object
    cv2.imshow( 'original', frame )
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert frame to HSV colorspace
    frame = cv2.inRange(frame, lower, upper) # Only show the values in the provided range
    #frame = cv2.blur( frame, (5,5) ) # Blur the frame
    cv2.imshow( 'frame', frame )
    # Quit with the "q" key!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
vs.stop()
