# Visual SLAM

The Visual SLAM component focuses on mapping and navigation of the construction environment. Visual SLAM uses images (video) for sensing the environment, and, on a high level, works on feature matching between adjacent frames. We use the Intel RealSense 435D as our visual sensor, which generates an RGB-D iamge used by the SLAM algorithm. Along with the RGB-D, we use the visual odometry and the Husky's IMU sensors (fused with an Extended Kalman Filter algorithm), for SLAM using by RTAB-Map, an open source Visual SLAM package. The ROS ```navigation stack``` uses the map generated by RTAB-Map and does path planning, and this information, along with the odometry, is used for moving the Husky in the environment using ```move_base```. We make use of ```tf``` and URDF files to link the coordinate systems of the ```base``` (Husky) and the ```camera``` (RealSense). This setup makes it easy for ```move_base``` to perform navigation.

<p align="center">
  <img src="/imgs/husky_perspective.jpg" />
</p>

# Hardware
- Clearpath Husky
- Intel RealSense D435
- Laptop with Clearpath Ubuntu 18.04

# Software
- ROS Melodic
- Rviz
- Clearpath Ubuntu 18.04
- realsense_ros [https://github.com/IntelRealSense/realsense-ros](https://github.com/IntelRealSense/realsense-ros)
- rtabmap_ros [http://wiki.ros.org/rtabmap_ros](http://wiki.ros.org/rtabmap_ros)
- move_base [http://wiki.ros.org/move_base](http://wiki.ros.org/move_base)

# Running the Visual SLAM and the navigation

```sh
roslaunch realsense2_camera liu_nav.launch
cd integration
python monitor_and_move.py
python control_k.py
```

<p align="center">
  <img width="500" height="400" src="/imgs/3d_map.png" />
</p>

<p align="center">
  <img width="500" height="400" src="/imgs/navigation.png" />
</p>
