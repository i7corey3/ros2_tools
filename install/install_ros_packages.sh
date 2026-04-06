#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

DIR="$(cd "$(dirname "$0")" && pwd)"

install_if_available() {
  local pkg="$1"
  if apt-cache show "$pkg" >/dev/null 2>&1; then
    echo "[OK] Installing $pkg"
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
      -o Dpkg::Options::="--force-confdef" \
      -o Dpkg::Options::="--force-confold" \
      "$pkg"
  else
    echo "[SKIP] Package not found: $pkg"
  fi
}

case "${1:-}" in
  install)
    DISTRO="${2:-}"
    if [[ -z "$DISTRO" ]]; then
      echo "Usage: $0 install <ros-distro>"
      exit 1
    fi

    export DEBIAN_FRONTEND=noninteractive
    export APT_LISTCHANGES_FRONTEND=none

    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get -y upgrade \
      -o Dpkg::Options::="--force-confdef" \
      -o Dpkg::Options::="--force-confold"

    # Package list
    PACKAGES=(
      ros-"$DISTRO"-ros2-control
      ros-"$DISTRO"-ros2-controllers
      ros-"$DISTRO"-rplidar-ros
      ros-"$DISTRO"-slam-toolbox
      ros-"$DISTRO"-navigation2
      ros-"$DISTRO"-nav2-bringup
      ros-"$DISTRO"-xacro
      ros-"$DISTRO"-imu-tools
      ros-"$DISTRO"-tf2-tools
      ros-"$DISTRO"-tf-transformations
      ros-"$DISTRO"-robot-localization
      ros-"$DISTRO"-image-geometry
      libserial-dev
      software-properties-common
      ros-"$DISTRO"-twist-mux
      ros-"$DISTRO"-spatio-temporal-voxel-layer
      ros-"$DISTRO"-gazebo-ros2-control
      ros-"$DISTRO"-gazebo-ros-pkgs
    )

    # Install safely
    for pkg in "${PACKAGES[@]}"; do
      install_if_available "$pkg"
    done

    # Handle wildcard packages safely
    for pattern in "ros-${DISTRO}-librealsense*" "ros-${DISTRO}-realsense2-*"; do
      matches=$(apt-cache search "^${pattern/\*/.*}" | awk '{print $1}') || true
      for pkg in $matches; do
        install_if_available "$pkg"
      done
    done

    # udev rules
    if [[ ! -f "/etc/udev/rules.d/99-realsense-libusb.rules" ]]; then
      if [[ -f "$DIR/99-realsense-libusb.rules" ]]; then
        sudo cp "$DIR/99-realsense-libusb.rules" /etc/udev/rules.d/
        sudo udevadm control --reload-rules && sudo udevadm trigger
      else
        echo "Warning: udev rule file not found at $DIR/99-realsense-libusb.rules"
      fi
    fi

    echo "Package install finished."
    ;;

  *)
    printf "Usage:\n\t./install_ros_packages.sh install humble\n"
    ;;
esac
