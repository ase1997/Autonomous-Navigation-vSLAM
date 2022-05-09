FROM arm64v8/ubuntu:18.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y software-properties-common git wget build-essential

RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add - &&\
    apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main' && \
    apt-get update && \
    apt-get install -y cmake

RUN apt-get install -y unzip

# OpenGL: Needed to install Pangolin
RUN apt-get install -y libgl1-mesa-dev libglew-dev

RUN apt-get install -y libxkbcommon-dev wayland-protocols

RUN apt-get clean

# Actual packages
RUN mkdir installs

# Catch2
RUN cd installs && \
    git clone -b v2.x https://github.com/catchorg/Catch2.git && \
    cd Catch2 && \
    cmake -Bbuild -H. -DBUILD_TESTING=OFF && \
    cmake --build build/ --target install

# Pangolin
RUN cd installs && \
    wget https://github.com/stevenlovegrove/Pangolin/archive/refs/tags/v0.5.zip && \
    unzip v0.5.zip && rm v0.5.zip && \
    cd Pangolin-0.5 && \
    mkdir build && \
    cd build && \
    cmake -DCPP11_NO_BOOSR=1 .. && \
    make -j

# Eigen3
RUN apt-get install -y libeigen3-dev

# OpenCV - Comment: This is for Docker with a clean environemtn only. JetPack has OpenCV 4.1
COPY ./nano_build_opencv installs/nano_build_opencv

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN cd installs/nano_build_opencv && \
    ./build_opencv.sh

# ORB_SLAM
COPY ./ORB_SLAM2 installs/ORB_SLAM2

RUN cd installs/ORB_SLAM2 && \
    chmod +x build.sh && \
    ./build.sh


# OpenCV
# RUN apt-get install -y libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
# RUN apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev

# RUN cd installs && \
#     git clone -b 3.4.16 https://github.com/opencv/opencv.git && \
#     git clone -b 3.4.16 https://github.com/opencv/opencv_contrib.git

# RUN sudo apt-get install libeigen3-dev

# ORB_SLAM
# RUN git clone https://github.com/raulmur/ORB_SLAM2.git ORB_SLAM2 && \
#    cd ORB_SLAM2 && \
#    chmod +x build.sh && \
#    ./build.sh
