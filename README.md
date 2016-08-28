# Sabercat Robotics Vision Processing Utilities

===============================================

Written in python, these vision processing libraries provide libraries for opencv 3.0 which is optimized to run on a raspberry pi 2. *Now on [Arch](https://archlinuxarm.org)*

## Install


[Install](https://www.continuum.io/downloads) Anaconda on your machine. This will give you numpy and python. Type ```python``` in your command prompt or terminal. You may be a windows elitist, and this may give you an error ```'python' is not a recognized internal or external command ... ``` if this happens, you need to add python to your ```PATH``` variable. Get help [here](http://stackoverflow.com/questions/20946025/unable-to-set-up-anaconda-on-windows-path-problems). This should bring up the python interactive REPL. You should be able to type code at the prompt of ```>>>``` Now you want to make sure that you have numpy installed. In the REPL, ```import numpy``` if you get an error, you need to install numpy. In the command line, ```conda install numpy``` This will go ahead and get you numpy.

[Install](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0) opencv 3.0 python for your machine.

After installing opencv on your machine, you will need the imutils module and pynetworktables module.
```python
  pip install imutils
  pip install pynetworktables
```

## Install on Raspberry Pi

~~Raspbian~~ *We changed OS to Arch* for frame rate reasons. Arch may be installed with the images provided in [this](https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=109545) forum thread. When you have Arch running, login to root with username: `root` and password: `root`

**BEFORE PROCEEDING, UPDATE SYSTEM** with `pacman -Syu`

### Install Dependencies

```pacman -S libjpeg-turbo```

```pacman -S python```

```pacman -S python-numpy```

```pacman -S python-pip```

```pacman -S opencv```

## About
--------

The saber_track module provides a robust method to track objects by way of HSV colorspace filtering. This is a very common method of tracking and is very useful in the **FIRST** championship.

## track.py
-----------

All of the functions of the *saber_track* Module can be demonstrated in the program ```track.py```. For a quick look at the command line options that the *track* program porvides, use ```python track.py --help``` This will give you the options and their description. The following will give a more detailed gist of its functionality.

## Video modes
--------------

The first thing you need is to give the program which camera to use. By default, the camera stream will be 0. If you have two webcams, you may change the vidmode to a different stream with the ```--vidmode``` tag.

If you're using an external usb webcam and your computer has a built-in webcam, you'll want to change try vidmode 1:
```sh
python track.py --vidmode 1
```
## Raw footage
--------------

In order to get the raw footage of the camera, you will want to add the raw tag to the program: ```python track.py --raw 1``` Using the raw tag will also be needed for recieving a video of the tracking bounding box.

## Filters
----------

The program uses colors to track objects. This means that it may get confused if there is a lot of 'noise' it the image. To tell the program which object it should track, we use filters. Filters are just a color reduction where we create an image from the camera stream where each pixel that falls within the color range will be white, and the pixels that are outside of the defined color range are black. We use sliders to adjust the color filters. In order to simplify the color space, we use [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV). HSV is a colorspace that stands for Hue, Saturation, and Value. We can tell the program to prompt trackbars that we may adjust in order to change the filtering range. To do this, simply use ```python track.py --raw 1 -f "my_filter"``` This will create a trackbar, masked image, and bounding box called *"my_filter"* The values set in the filter's trackbars will be used to find the bounding box of the object.

You can use multiple filters by putting spaces in the ```-f``` tag like so: ```python track.py --raw 1 -f "filter_one filter_two"``` this will create two filters, one called *"filter_one"* and the other called *"filter_two"* You will be greeted with two masked windows and trackbars.

## I/O Support
--------------

```track.py``` and therefore saber_track support saving and loading hsv colorspaces. This way, you may adjust the hsv limits before the competition and adjust for competition lighting and then use that same file for the actual game. Use the ```-i``` or ```--input``` tags for inputing ```.json``` files. Use the ```-o``` or ```--output``` tags for setting the output file. *You do not have to add the .json file extention to the file name when using these tags*

We use json as a human readable and writable serialization method. Take advantage of that.

### Game Example
----------------

You'll want to adjust the color space in the enviroment you will use it in. This means you need to tweak the hsv values on game day in order to adjust for lighting and unusual noise.

For instance if you are trying to track the goal, you should go to the practice match and adjust the HSV values.

```
python track.py --raw 1 -f "goal" -o goal_file
```

This will generate a track file when you **QUIT THE SESSION WITH THE Q KEY** If you didn't notice the bold caps, you need to use the q key on exit. You cannot use the keyboard disrupts that command lines have.

If you generated that file without the raspberry pi, you may transfer the file to the [scp](http://support.real-time.com/linux/web/scp.html) utility.

Your pi will likely be onboard the robot in order to reduce latency. This means that you cannot go through default boot prosedures. You will need to create a bash [script](https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=61782) which starts the vision program.

In that script you will want to have some load command.

```
python track.py -n -i goal_file -p <networktable ip here>
```

You may be wondering, "where the hell did the ```-n``` an ```-p``` tags come from?"
Well, the ```-n``` tag stands for no display. This means that the program will not initialize any windows.
The ```-p``` tag will set the ip of the network tables so that you can get the bounding box values of the goal. To get the gist of everything, use ```python track.py -h``` to see options in help.
## Log files

The debug log generated should be located in ```debug_log.log```

## Versions
------------------
*0.0.4* Switched to json track serialization. Runs on arch now
*0.0.3* Added tagging support. Fixed bugs. Cleaned code. Added more documentation.
*0.0.2* Added multiple filtering capabilities.
*0.0.1* Added more modes and file I/O. Cleaned code.
*0.0.0* Base opencv HSV filtering and trackbar
### Current utilities include:

- ```installcv.bash``` installation script for opencv on raspberry pi *(Thanks to: Thomas Cyrix)*
- ```log.py``` is a simple logging module for streamlined debugging and records (cv2 independent)
- ```saber_track.py``` The main module for video tracking
- ```track.py``` A small test script showing off the saber_track module


### Planned Implementation:
 - distance calculation
 - high preformance distribution for the Raspberry pi

 ### TODO:
 - Update Documentation
 - code cleanup
 - code optimization
 - gpgpu acceleration
 - raspberry pi usb webcam latency fix

[contact](mailto:sabercatrobotics@gmail.com)
