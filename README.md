# Sabercat Robotics Vision Processing Utilities

===============================================

Written in python, these vision processing libraries provide libraries for opencv 3.0 which is optimized to run on a raspberry pi 2. [Install](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0) opencv python.

```python
  pip install imutils
```

## Current utilities include:

- ```installcv.bash``` installation script for opencv on raspberry pi *(Thanks to: Thomas Cyrix)*
- ```log.py``` is a simple logging module for streamlined debugging and records (cv2 independent)
- ```color_seperation.py``` is a simple application for filtering HSV colorspace values with RGB sliders.


## Planned Implementation:

 - video color picker with box selection
 - value pipline to driverstation code
 - distance calculation
 - tracking box for stronghold balls
 -  goal tracking
