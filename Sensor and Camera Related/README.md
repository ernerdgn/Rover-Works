# SENSOR AND CAMERA RELATED

In this section you can find jobs that using the data obtained from sensors and cameras.

Most of the camera data is getting from ZED2, you can find more in [here](https://www.stereolabs.com/zed-2/)
and official documentation [here](https://www.stereolabs.com/docs/).

### bounder.py
This program makes LiDAR to scan 180° instead of 360°.

### aruco_gate_passer.py
This program calculates a reliable path to pass from a gate that will be defined by two ArUco markers.

1- Think of two points in the cartezian coordinate system,

2- find the mid-point,

3- draw the line that passes trough the ArUco's points,

4- draw another line that is perpendicular to the first line and passes trough the mid-point,

5- take desired units(for example 3) lower and higher,

6- send the coordinat informations to robot.
