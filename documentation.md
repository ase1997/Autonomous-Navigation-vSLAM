-------Add #include<unistd.h>-------
/src
       System
       Tracking
       Viewer
       LocalMapping
       LoopClosing
/Examples
       /Monocular
               mono_euroc
               mono-kitti
               mono-tum
       /Stereo
               stereo_euroc
               stereo_kitti
       /RGB-D
               rgbd_tum
------------------------------------

------------------------------------
replace opencv/cv.h with the following
        #include<opencv2/imgproc/imgproc_c.h>
        #include <opencv2/highgui/highgui_c.h>#include<opencv2/imgproc/imgproc_c.h>
in these files
/include
        ORBextractor

Make ROS topics accessible over a network
1. Add the IP address and username to /etc/hosts -> xxx.xxx.xx.x vslam
2. export ROS_MASTER_URI=http://vslam:11311


## rtabmap docker
https://github.com/introlab/rtabmap_ros/issues/617
https://github.com/introlab/rtabmap_ros/tree/master/docker
https://github.com/introlab/rtabmap/wiki/Installation#rtab-map-desktop-ubuntu-1804-2004


REALSENSE and ORBSLAM2 on ROS

Intel RealSense SDK: https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md
and
https://github.com/IntelRealSense/realsense-ros#installation-instructions
sudo apt-get install ros-melodic-rgbd-launch
export ROS_HOSTNAME=localhost
export ROS_MASTER_URI=http://localhost:11311
Now, it works in rviz

Change the file: Examples/ROS/ORB_SLAM2/src/ros_rgbd.cc
// message_filters::Subscriber<sensor_msgs::Image> rgb_sub(nh, "/camera/rgb/image_raw", 1);
// message_filters::Subscriber<sensor_msgs::Image> depth_sub(nh, "camera/depth_registered/image_raw", 1);
message_filters::Subscriber<sensor_msgs::Image> rgb_sub(nh, "/camera/color/image_raw", 1);
message_filters::Subscriber<sensor_msgs::Image> depth_sub(nh, "/camera/aligned_depth_to_color/image_raw", 1);

Build with ROS: ./build_ros.sh

Now ORB_SLAM2 can access RealSense
rosrun ORB_SLAM2 RGBD Vocabulary/ORBvoc.txt RealSense.yaml

-------------------------------------------------------
---2022-02-21--------
install ROS melodic
install catkin build sudo apt-get install ros-melodic-catkin python-catkin-tools
install realsense sdk https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation
install realsense rgbd sudo apt install ros-melodic-rgbd-launch
create catkin_ws folder
download realsense ros wrapper and ORBSLAM2 wrapper into src folder  https://github.com/IntelRealSense/realsense-ros  https://github.com/rayvburn/ORB-SLAM2_ROS  (official orbslam2_ros https://github.com/appliedAI-Initiative/orb_slam_2_ros)
into ORBSLAM2 folder change source code, message_filters and camera info
into cv_bridge file, change opencv version /opt/ros/melodic/share/cv_bridge/cmake/cv_bridgeConfig.cmake
back to catkin folder and do catkin build
source the setup bash files
rosrun 1) realsense rgbd 2) orbslam2 3)rviz
roslaunch realsense2_camera rs_rgbd.launch
roslaunch realsense2_camera rs_rgbd.launch align_depth:=true depth_width:=320 depth_height:=240 depth_fps:=15 color_width:=320 color_height:=240 color_fps:=15
roslaunch orb_slam2_ros orb_slam2_d435_rgbd.launch
rosrun tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link camera_link

depthimage_to_laserscan and gmapping
install depthimage_to_laserscan: sudo apt install ros-melodic-depthimage-to-laserscan
install gmapping: sudo apt-get install ros-melodic-slam-gmapping
Run depthimage_to_laserscan: rosrun depthimage_to_laserscan depthimage_to_laserscan image:=/camera/depth/image_rect_raw
Publish a static transform: rosrun tf static_transform_publisher 0.0 0.0 0.0 0 0 0 /map camera_depth_frame 100
Run gmapping: rosrun gmapping slam_gmapping scan:=scan _base_frame:=camera_depth_frame _linearUpdate:=0.0 _angularUpdate:=0.0
References:
https://answers.ros.org/question/102966/gmapping-issues-with-laser-pose/
https://answers.ros.org/question/230608/slam_gmapping-stop-at-registering-first-scan/