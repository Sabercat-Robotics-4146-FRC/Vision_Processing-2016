import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import argparse
from log import Log
from saber_track import Tracker
import argparse
import json

def flag_it( value ):
    return not value == None
# Parse some command line arguments!
parser = argparse.ArgumentParser(description='HSV color sliders for video.')
parser.add_argument('-s', '--settings', dest='st', type=str, help='The .json settings file', default="" )

args = parser.parse_args()

if not args.st == "":
    with open( args.st + ".json")as data_file:
        settings = json.loads(data_file.read())
else:
    raise Exception("Please provide settings")

log = Log(settings["log_name"])
log.debug("Mode: " + str(settings["vidmode"]) )
vs = WebcamVideoStream(src=int(settings["vidmode"])).start() # Initialize the camera object on a seperate I/O thread

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
