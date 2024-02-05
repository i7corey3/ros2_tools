source /opt/ros/$ROS_DISTRO/setup.bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
WS="$(dirname "$DIR")"
cd $DIR

if [ "$3" == "test" ]; 
then
    printf "The node name test is reserved and not allowed\n"
    exit 1
fi
if [ "$2" == "test" ]; 
then
    printf "The package name test is reserved and not allowed\n"
    exit 1
fi

case $1 in
    python)
        ros2 pkg create --build-type ament_python $2
        mv $2 $WS/src
        python3 $PWD/buildNode.py $2 python $3
    ;;
    c++)
        ros2 pkg create --build-type ament_cmake $2
        mv $2 $WS/src
        python3 $PWD/buildNode.py $2 c++ $3
    ;;
    *)
        printf "Type python or c++ then the package name and node name\n\nexample:\n\t./createPackage python package_name node_name\n\n"
    ;;
esac
cd ../