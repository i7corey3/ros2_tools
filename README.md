# ros2_tools

This repository expands on the ros2 node creations command that will setup majority of the ros related code including:
- Creating config folder with param file
- Creating launch folder with an auto generated launch file ready to use
- Creates a generic node file linked to the ros2 command
- Works for both python anc c++ nodes
- Available for ros2 on Linux and Windows

## How To Use

Add both the createPackage and buildNode files to your src/ folder 
> createPackage.sh in using ros on Linux, createPackage.bat for Windows

This script takes in three arguments <code_language> <package_name> <node_name>

To create an example node in python run:

```
./createPackage.sh python <package_name> <node_name>
```

To create an example package in c++ run:

```
./createPackage.sh c++ <package_naem> <node_name>
```

