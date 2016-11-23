import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import argparse
from log import Log
from saber_track import Tracker
import argparse

def flag_it( value ):
    if value == None:
        return False
    else:
        return True

# Parse some command line arguments!
parser = argparse.ArgumentParser(description='HSV color sliders for video.')
parser.add_argument('-v', '--vidmode', dest='vidmode', type=int, help='Usage: \"--video_mode 0\" for webcam', default=0 )
parser.add_argument('-i', '--input', dest='input', type=str, help='The .track input file', default="" )
parser.add_argument('-o', '--output', dest='output', type=str, help='The .track output file', default="" )
parser.add_argument('-f', '--filters', help='Enable the trackbar with filters', default = "" )
parser.add_argument('-n', '--nodisplay', help='Weather to display images' )
parser.add_argument('--hsv', help='Weather to display hsv' )
parser.add_argument('--raw', help='Weather to display raw footage' )
parser.add_argument('-p', '--port', help='Which port to use for the networktables', default="" )
args = parser.parse_args()

r_flag = flag_it( args.raw )
hsv_flag = flag_it( args.hsv )
dis_flag = not flag_it( args.nodisplay )
log = Log("debug_log")
vs = WebcamVideoStream(src=args.vidmode).start() # Initialize the camera object on a seperate I/O thread
settings = {
    "port" : args.port,
    "filters": args.filters,
    "hsv": hsv_flag,
    "original": r_flag,
    "display": dis_flag,
    "in_file": args.input,
    "out_file": args.output,
}
#port=args.port,filters=args.filters,hsv=hsv_flag,original=r_flag,display=dis_flag,in_file=args.input, out_file=args.output
st = Tracker( vs, log, settings )

while True:
    st.update()
    # Quit with the "q" key!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Write to the file before closing logs. TODO: optional: logless usage
        st.save()
        log.kill("User Invoked Safe Quit")
        break
cv2.destroyAllWindows()
vs.stop()
