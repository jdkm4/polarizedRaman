arduinoReader.py: Reads outputs from the arduino and averages them.

calibrater.py: An attempt to get the motors to automatically calibrate themselves. Probably no longer necessary.

dataCollection.py: Older version of fastDataColection.py

ell.py: Allows for manual control of ELL motors

fastDataColection.py: Used to test motors/optics, will rotate an optics piece by a certain number of degrees and read the value from the Arduino each time, and then create a plot and csv file with the data.

gui.py: GUI for the project. Currently does not actually control the motors at all.

kin.py: Allows for manual control of kinesis motors. No longer necessary.

main.py: Allows for manual control of both ELL and kinesis motors. No longer necessary.

rotator.py: An attempt to combine calibrater.py and main.py in such a way that specific configurations of optics can be entered in and the motors will rotate to reach those configurations.

sketch_jun30a.ino: Code for the Arduino which reads off data from the photodetector.
