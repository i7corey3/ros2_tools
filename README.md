# ros2_tools

This repository expands on the ros2 package creations commands by auto generating majority of the ros2 related code including:
- Creating a config folder with an auto generated parameters file
- Creating a launch folder with an auto generated launch file ready to use
- Creates a generic node file linked with the ros2 command
- Works with both python and c++ packages
- Available for ros2 on Linux and Windows

## How To Use

Add both the createPackage and buildNode files to your ros2 workspace 

> createPackage.sh if using ros2 on Linux, createPackage.bat for Windows


This script takes in three arguments <code_language> <package_name> <node_name>

To create an example package in python run:

```
./createPackage.sh python <package_name> <node_name>
```

To create an example package in c++ run:

```
./createPackage.sh c++ <package_naem> <node_name>
```

### Notes

Currently the windows createPackage.bat file only works with ros2 galactic 

If you have another ros2 distro change the following line to the correct path inside the createPackage.bat file

```
call C:\opt\ros\galactic\x64\setup.bat
```
