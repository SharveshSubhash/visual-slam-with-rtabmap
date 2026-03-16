from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        parameters=[{
            'enable_imu_fusion': False,
            'enable_rectified_pose': False,
            'denoise_input_images': False,
            'rectify_input_images': True,
            'base_frame': 'camera_link',
            # Tell SLAM to look for the Left and Right IR frames
            'camera_optical_frames': [
                'camera_infra1_optical_frame',
                'camera_infra2_optical_frame',
            ],
        }],
        remappings=[
            # Map Left IR to image_0
            ('visual_slam/image_0', '/camera/camera/infra1/image_rect_raw'),
            ('visual_slam/camera_info_0', '/camera/camera/infra1/camera_info'),
            # Map Right IR to image_1
            ('visual_slam/image_1', '/camera/camera/infra2/image_rect_raw'),
            ('visual_slam/camera_info_1', '/camera/camera/infra2/camera_info')
        ]
    )

    visual_slam_container = ComposableNodeContainer(
        name='visual_slam_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[visual_slam_node],
        output='screen'
    )

    return LaunchDescription([visual_slam_container])
