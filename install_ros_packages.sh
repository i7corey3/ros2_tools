DIR="$( cd "$( dirname "$0" )" && pwd )"

case $1 in
    install)
        sudo apt-get update && sudo apt-get upgrade -y 
        sudo apt-get install ros-$2-ros2-control -y
        sudo apt-get install ros-$2-ros2-controllers -y
        sudo apt-get install ros-$2-rplidar-ros -y
        sudo apt-get install ros-$2-slam-toolbox -y
        sudo apt-get install ros-$2-navigation2 -y
        sudo apt-get install ros-$2-nav2-bringup -y
        sudo apt-get install ros-$2-xacro -y
        sudo apt-get install ros-$2-librealsense* -y
        sudo apt-get install ros-$2-realsense2-* -y
        sudo apt-get install ros-$2-imu-tools -y
        sudo apt-get install ros-$2-tf2-tools -y
        sudo apt-get install ros-$2-tf-transformations -y
        sudo apt-get install ros-$2-robot-localization -y
        sudo apt-get install ros-$2-image-geometry -y
        sudo apt-get install libserial-dev -y
        sudo apt-get install software-properties-common -y
        sudo apt-get install ros-$2-twist-mux -y
        sudo apt-get install ros-$2-spatio-temporal-voxel-layer -y
        sudo apt-get install ros-$2-gazebo-ros2-control -y
        sudo apt-get install ros-$2-gazebo-ros-pkgs -y
        if [ ! -f "/etc/udev/rules.d/99-realsense-libusb.rules" ]; then
            sudo cp $DIR/files/99-realsense-libusb.rules /etc/udev/rules.d/
            sudo udevadm control --reload-rules && udevadm trigger
        fi
    ;;
    *)
        printf "Type install then the ros distro to install the common ros packages for robot development\n\nexample:\n\t./install_ros_packages.sh install humble\n\n"
    ;;
esac






