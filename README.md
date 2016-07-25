# Sabercat Robotics Vision Processing Utilities

===============================================

Written in python, these vision processing libraries provide libraries for opencv 3.0 which is optimized to run on a raspberry pi 2.

## Install


[Install](https://www.continuum.io/downloads) Anaconda on your machine. This will give you numpy and python. Type ```python``` in your command prompt or terminal. You may be a windows elitist, and this may give you an error ```'python' is not a recognized internal or external command ... ``` if this happens, you need to add python to your ```PATH``` variable. Get help [here](http://stackoverflow.com/questions/20946025/unable-to-set-up-anaconda-on-windows-path-problems). This should bring up the python interactive REPL. You should be able to type code at the prompt of ```>>>``` Now you want to make sure that you have numpy installed. In the REPL, ```import numpy``` if you get an error, you need to install numpy. In the command line, ```conda install numpy``` This will go ahead and get you numpy.

[Install](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0) opencv 3.0 python for your machine.

After installing opencv on your machine, you will need the imutils module.
```python
  pip install imutils
```

## Install on Raspberry Pi

Just run the ```installcv.bash``` script written by Thomas Cyrix and updated for gui by GowanR.
```sh
bash installcv.bash
```

## Example usage of the saber_track module

The saber_track module provides a robust method to track objects by way of HSV colorspace filtering. This is a very common method of tracking and is very useful in the **FIRST** championship.

To get a taiste of what the current version accomplishes, you can run the ```test_tracker.py``` script like so:

```sh
python test_tracker.py
```
If you're using an external usb webcam and your computer has a built-in webcam, you'll want to change the vidmode:
```sh
python test_tracker.py --vidmode 1
```

You will be prompted with four windows. An original video, a HSV converted video, a filtered video, and a slider window that you may use to adjust the hsv filters

### Example: Desk Toys

![original]("https://github.com/Sabercat-Robotics-4146-FRC/Vision_Processing-2016/blob/master/img/original.PNG")

The original image.

![trackbar]("https://github.com/Sabercat-Robotics-4146-FRC/Vision_Processing-2016/blob/master/img/trackbar.PNG")

I adjusted the trackbar so that to filter the original image.

![filtered]("https://github.com/Sabercat-Robotics-4146-FRC/Vision_Processing-2016/blob/master/img/filtered.PNG")

The filtered image.

#### For the Raspberry pi, use

```sh
python3 test_tracker.py
```

You can get the log files produced for this pocess in a file called ```debug_log.log```

### Current utilities include:

- ```installcv.bash``` installation script for opencv on raspberry pi *(Thanks to: Thomas Cyrix)*
- ```log.py``` is a simple logging module for streamlined debugging and records (cv2 independent)
- ```saber_track.py``` The main module for video tracking
- ```test_tracker.py``` A small test script showing off the saber_track module


### Planned Implementation:

 - video color picker with box selection
 - value pipline to driverstation code
 - distance calculation
 - efficient tracking box for stronghold balls
 - efficient goal tracking
