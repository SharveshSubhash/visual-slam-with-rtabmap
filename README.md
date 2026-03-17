# Semantic SLAM Architecture: Isaac ROS & Intel RealSense D415

This repository contains a decoupled, hardware-accelerated Visual SLAM and 3D mapping pipeline built for ROS 2 Humble. It bridges an Intel RealSense D415 RGB-D camera with NVIDIA's hardware-accelerated cuVSLAM (TensorRT) and RTAB-Map for spatial memory.

## Architecture Overview
* **Hardware:** Lenovo Legion (RTX 4060), Intel RealSense D415
* **Odometry (cuVSLAM):** Utilizes the D415's hidden Left/Right Infrared streams (`infra1`, `infra2`) mapped via a custom launch file to provide high-speed, 6-DOF tracking.
* **Spatial Memory (RTAB-Map):** Subscribes to the cuVSLAM odometry, RGB, and Aligned Depth topics to stitch a persistent, colorized 3D MapCloud, entirely bypassing internal visual odometry to save CPU overhead.

## Custom Configurations Included
* **Docker Environment:** The `Dockerfile.ros2_humble` has been permanently modified to include `realsense2_camera`, `isaac_ros_visual_slam`, and `rtabmap_ros`.
* **Launch Files:** Includes a custom `d415_vslam_subscriber.launch.py` to correctly map the D415 optical frames and disable IMU fusion (as the D415 lacks an internal IMU).

## Quick Start Guide

### 1. Launch the Environment
```bash
export ISAAC_ROS_WS=~/workspaces/isaac_ros-dev
cd ${ISAAC_ROS_WS}/src/isaac_ros_common
./scripts/run_dev.sh```

## 2. Launch the Pipeline (Requires 3 Terminals)
### Terminal 1: Camera Node (Forcing Hardware Synchronization)
```bash
ros2 launch realsense2_camera rs_launch.py enable_infra1:=true enable_infra2:=true enable_color:=true enable_depth:=true align_depth.enable:=true pointcloud.enable:=false enable_sync:=true depth_module.profile:=640x480x30 rgb_camera.profile:=640x480x30 enable_gyro:=false enable_accel:=false
```

### Terminal 2: cuVSLAM Engine
```bash
ros2 launch isaac_ros_visual_slam d415_vslam_subscriber.launch.py
```

### Terminal 3: RTAB-Map
```bash
ros2 launch rtabmap_launch rtabmap.launch.py \
  rtabmap_args:="--delete_db_on_start" \
  rgb_topic:=/camera/camera/color/image_raw \
  depth_topic:=/camera/camera/aligned_depth_to_color/image_raw \
  camera_info_topic:=/camera/camera/color/camera_info \
  odom_topic:=/visual_slam/tracking/odometry \
  visual_odometry:=false \
  frame_id:=camera_link \
  approx_sync:=true \
  qos:=2
```

