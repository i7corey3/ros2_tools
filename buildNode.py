import os
import sys
import yaml
import shutil
from pathlib import Path


def camel_case(s):
    new_string = ""
    temp = s.split("_")
    for st in temp:
        if st:
            new_string += st[0].upper() + st[1:]
    return new_string


def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)


def safe_rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def safe_unlink(path):
    if os.path.exists(path):
        os.remove(path)


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in lines:
            f.write(line if line.endswith("\n") else line + "\n")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def insert_after(lines, needle, new_lines):
    if isinstance(new_lines, str):
        new_lines = [new_lines]

    for i, line in enumerate(lines):
        if needle in line:
            for offset, new_line in enumerate(new_lines):
                lines.insert(
                    i + 1 + offset,
                    new_line if new_line.endswith("\n") else new_line + "\n",
                )
            return True
    return False


def insert_before(lines, needle, new_lines):
    if isinstance(new_lines, str):
        new_lines = [new_lines]

    for i, line in enumerate(lines):
        if needle in line:
            for offset, new_line in enumerate(new_lines):
                lines.insert(
                    i + offset,
                    new_line if new_line.endswith("\n") else new_line + "\n",
                )
            return True
    return False


def createNodePython(name, node):
    path = f"{Path(__file__).resolve().parents[1]}/src"
    pkg_dir = f"{path}/{name}"
    module_dir = f"{pkg_dir}/{name}"

    safe_mkdir(module_dir)
    safe_mkdir(f"{pkg_dir}/config")
    safe_mkdir(f"{pkg_dir}/launch")
    safe_mkdir(f"{pkg_dir}/resource")

    with open(f"{module_dir}/__init__.py", "w", encoding="utf-8", newline="\n") as f:
        f.write("")

    with open(f"{pkg_dir}/resource/{name}", "w", encoding="utf-8", newline="\n") as f:
        f.write("")

    data = [
        "import rclpy",
        "from rclpy.node import Node",
        "import time",
        "",
        "",
        f"class {camel_case(name)}(Node):",
        "    def __init__(self):",
        f"        super().__init__('{node}')",
        "",
        "        self.declare_parameters(",
        '            namespace="",',
        "            parameters=[",
        "",
        "            ]",
        "        )",
        "",
        '        self.sim_time = self.get_parameter("use_sim_time").get_parameter_value().bool_value',
        "",
        '        self.get_logger().info(f"sim_time is set to {self.sim_time}")',
        "",
        "        time.sleep(1)",
        "",
        "",
        "",
        "def main(args=None):",
        "    rclpy.init(args=args)",
        "",
        f"    {name} = {camel_case(name)}()",
        "",
        f"    rate = {name}.create_rate(20)",
        "    while rclpy.ok():",
        f"        rclpy.spin_once({name})",
        "",
        f"    {name}.destroy_node()",
        "    rclpy.shutdown()",
        "",
        "",
        'if __name__ == "__main__":',
        "    main()",
    ]
    write_lines(f"{module_dir}/{node}.py", data)

    setup_py = [
        "from glob import glob",
        "import os",
        "",
        "from setuptools import find_packages, setup",
        "",
        f'package_name = "{name}"',
        "",
        "setup(",
        "    name=package_name,",
        '    version="0.0.0",',
        '    packages=find_packages(exclude=("test",)),',
        "    data_files=[",
        '        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),',
        '        (f"share/{package_name}", ["package.xml"]),',
        '        (f"share/{package_name}/launch", glob(os.path.join("launch", "*launch.[pxy][yma]*"))),',
        '        (f"share/{package_name}/config", glob(os.path.join("config", "*[yaml]*"))),',
        "    ],",
        '    install_requires=["setuptools"],',
        "    zip_safe=True,",
        "    maintainer='maintainer',",
        "    maintainer_email='maintainer@example.com',",
        '    description="Auto-generated ROS 2 Python package",',
        '    license="Apache-2.0",',
        "    entry_points={",
        "        'console_scripts': [",
        f"            '{node} = {name}.{node}:main',",
        "        ],",
        "    },",
        ")",
    ]
    write_lines(f"{pkg_dir}/setup.py", setup_py)

    params = {
        node: {
            "ros__parameters": {
                "use_sim_time": False
            }
        }
    }
    with open(f"{pkg_dir}/config/params.yaml", "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(params, f, sort_keys=False)

    launch_file = [
        "import os",
        "",
        "from ament_index_python.packages import get_package_share_directory",
        "from launch.substitutions import LaunchConfiguration",
        "from launch.actions import DeclareLaunchArgument",
        "from launch import LaunchDescription",
        "from launch_ros.actions import Node",
        "from pathlib import Path",
        "",
        "",
        "def generate_launch_description():",
        "",
        f"    package_name = '{name}'",
        "",
        "    params_file = os.path.join(get_package_share_directory(package_name), 'config', 'params.yaml')",
        "    cwd = f'{Path(__file__).parents[5]}/src/{package_name}/config/params.yaml'",
        "    os.system(f'cp {cwd} {params_file}')",
        "",
        f"    {name} = Node(",
        "        package=package_name,",
        f"        executable='{node}',",
        "        parameters=[params_file]",
        "",
        "    )",
        "",
        "    return LaunchDescription([",
        f"        {name}",
        "    ])",
    ]
    write_lines(f"{pkg_dir}/launch/{name}.launch.py", launch_file)


def createNodeCpp(name, node):
    path = f"{Path(__file__).resolve().parents[1]}/src"
    pkg_dir = f"{path}/{name}"

    safe_mkdir(f"{pkg_dir}/src")
    safe_mkdir(f"{pkg_dir}/config")
    safe_mkdir(f"{pkg_dir}/launch")

    cpp_file = [
        "#include <iostream>",
        "#include <chrono>",
        "#include <functional>",
        "#include <memory>",
        "#include <string>",
        "#include <vector>",
        "#include <ament_index_cpp/get_package_share_directory.hpp>",
        "",
        "",
        '#include "rclcpp/rclcpp.hpp"',
        "",
        "using namespace std::chrono_literals;",
        "",
        f"class {camel_case(name)} : public rclcpp::Node",
        "{",
        "",
        "    public:",
        f"       {camel_case(name)}()",
        f'        : Node("{node}")',
        "        { }",
        "",
        "",
        "};",
        "",
        "",
        "int main(int argc, char * argv[])",
        "{",
        "    rclcpp::init(argc, argv);",
        f"    rclcpp::spin(std::make_shared<{camel_case(name)}>());",
        "    rclcpp::shutdown();",
        "",
        "    return 0;",
        "}",
    ]
    write_lines(f"{pkg_dir}/src/{node}.cpp", cpp_file)

    cmake = [
        "cmake_minimum_required(VERSION 3.8)",
        f"project({name})",
        "",
        "if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES \"Clang\")",
        "  add_compile_options(-Wall -Wextra -Wpedantic)",
        "endif()",
        "",
        "# find dependencies",
        "find_package(ament_cmake REQUIRED)",
        "find_package(rclcpp REQUIRED)",
        "find_package(std_msgs REQUIRED)",
        "# uncomment the following section in order to fill in",
        "# further dependencies manually.",
        "# find_package(<dependency> REQUIRED)",
        "",
        "if(BUILD_TESTING)",
        "  find_package(ament_lint_auto REQUIRED)",
        "  # the following line skips the linter which checks for copyrights",
        "  # comment the line when a copyright and license is added to all source files",
        "  set(ament_cmake_copyright_FOUND TRUE)",
        "  # the following line skips cpplint (only works in a git repo)",
        "  # comment the line when this package is in a git repo and when",
        "  # a copyright and license is added to all source files",
        "  set(ament_cmake_cpplint_FOUND TRUE)",
        "  ament_lint_auto_find_test_dependencies()",
        "endif()",
        "include_directories(include)",
        " ",
        "set(dependencies",
        "    rclcpp",
        "    std_msgs",
        ")",
        " ",
        "## COMPILE",
        "add_library(",
        "    ${PROJECT_NAME}",
        "    SHARED",
        f"    src/{node}.cpp",
        ")",
        " ",
        "target_include_directories(",
        "    ${PROJECT_NAME}",
        "    PRIVATE",
        "    include",
        ")",
        " ",
        "ament_target_dependencies(",
        "    ${PROJECT_NAME}",
        "    PUBLIC",
        "    ${dependencies}",
        " ",
        ")",
        " ",
        "add_executable(",
        f"    {node}",
        f"    src/{node}.cpp",
        ")",
        " ",
        f"ament_target_dependencies({node} ${{dependencies}})",
        " ",
        "install(",
        "    TARGETS",
        "    ${PROJECT_NAME}",
        "    DESTINATION lib/${PROJECT_NAME}",
        ")",
        " ",
        "# INSTALL",
        "install(",
        "    TARGETS ",
        f"    {node}",
        "    DESTINATION lib/${PROJECT_NAME}",
        ")",
        " ",
        "install(DIRECTORY",
        "launch",
        "DESTINATION share/${PROJECT_NAME}/",
        ")",
        " ",
        "install(DIRECTORY",
        "config",
        "DESTINATION share/${PROJECT_NAME}/",
        ")",
        " ",
        "ament_export_include_directories(",
        "    include",
        ")",
        " ",
        "ament_export_libraries(",
        "    ${PROJECT_NAME}",
        ")",
        " ",
        "ament_export_dependencies(",
        "    ${dependencies}",
        ")",
        " ",
        " ",
        "ament_export_include_directories(include)",
        "",
        "ament_package()",
    ]
    write_lines(f"{pkg_dir}/CMakeLists.txt", cmake)

    params = {
        node: {
            "ros__parameters": {
                "use_sim_time": False
            }
        }
    }
    with open(f"{pkg_dir}/config/params.yaml", "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(params, f, sort_keys=False)

    launch_file = [
        "import os",
        " ",
        "from ament_index_python.packages import get_package_share_directory",
        "from launch.substitutions import LaunchConfiguration",
        "from launch.actions import DeclareLaunchArgument",
        "from launch import LaunchDescription",
        "from launch_ros.actions import Node",
        " ",
        " ",
        "def generate_launch_description():",
        " ",
        f"    package_name = '{name}'",
        " ",
        "    params_file = os.path.join(get_package_share_directory(package_name), 'config', 'params.yaml')",
        " ",
        f"    {name} = Node(",
        "        package=package_name,",
        f"        executable='{node}',",
        "        parameters=[params_file]",
        " ",
        "    )",
        " ",
        "    return LaunchDescription([",
        f"        {name}",
        "    ])",
    ]
    write_lines(f"{pkg_dir}/launch/{name}.launch.py", launch_file)


def createMainPackage(name):
    path = f"{Path(__file__).resolve().parents[1]}/src"
    pkg_dir = f"{path}/{name}"

    cmake_path = f"{pkg_dir}/CMakeLists.txt"
    if os.path.exists(cmake_path):
        data = read_lines(cmake_path)
    else:
        data = [
            "cmake_minimum_required(VERSION 3.8)\n",
            f"project({name})\n",
            "\n",
            "if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES \"Clang\")\n",
            "  add_compile_options(-Wall -Wextra -Wpedantic)\n",
            "endif()\n",
            "\n",
            "# find dependencies\n",
            "find_package(ament_cmake REQUIRED)\n",
            "ament_package()\n",
        ]

    install_block = [
        "",
        "install(",
        "    DIRECTORY config description launch worlds",
        "    DESTINATION share/${PROJECT_NAME}",
        ")",
        "",
    ]
    if "install(\n    DIRECTORY config description launch worlds" not in "".join(data):
        insert_before(data, "ament_package()", install_block)

    write_lines(cmake_path, data)

    safe_rmtree(f"{pkg_dir}/include")
    safe_rmtree(f"{pkg_dir}/src")

    safe_mkdir(f"{pkg_dir}/config")
    safe_mkdir(f"{pkg_dir}/launch")
    safe_mkdir(f"{pkg_dir}/description")
    safe_mkdir(f"{pkg_dir}/worlds")

    xacro_robot = [
        '<?xml version="1.0"?>',
        f'<robot xmlns:xacro="http://www.ros.org/wiki/xacro"  name="{name}">',
        '<xacro:arg name="use_ros2_control" default="true"/>',
        f'<xacro:include filename="{name}_core.xacro" />',
        '<xacro:if value="$(arg use_ros2_control)">',
        '    <xacro:include filename="ros2_control.xacro" />',
        '</xacro:if>',
        '<xacro:unless value="$(arg use_ros2_control)">',
        '    <xacro:include filename="gazebo_control.xacro" />',
        '</xacro:unless>',
        '',
        '</robot>',
    ]
    write_lines(f"{pkg_dir}/description/{name}.urdf.xacro", xacro_robot)

    xacro_core = [
        '<?xml version="1.0"?>',
        '<robot xmlns:xacro="http://www.ros.org/wiki/xacro">',
        "",
        '<xacro:include filename="inertial_macros.xacro"/>',
        "",
        '<!-- BASE LINK -->',
        '<link name="base_link">',
        '</link>',
        '<!-- BASE_FOOTPRINT LINK -->',
        '<joint name="base_footprint_joint" type="fixed">',
        '    <parent link="base_link"/>',
        '    <child link="base_footprint"/>',
        '    <origin xyz="0 0 0" rpy="0 0 0"/>',
        '</joint>',
        '<link name="base_footprint">',
        '</link>',
        "",
        "",
        '</robot>',
    ]
    write_lines(f"{pkg_dir}/description/{name}_core.xacro", xacro_core)

    shutil.copy(f"{os.path.dirname(__file__)}/files/inertial_macros.xacro", f"{pkg_dir}/description/")
    shutil.copy(f"{os.path.dirname(__file__)}/files/ros2_control.xacro", f"{pkg_dir}/description/")

    ros2_control_path = f"{pkg_dir}/description/ros2_control.xacro"
    if os.path.exists(ros2_control_path):
        data = read_lines(ros2_control_path)
        insert_after(
            data,
            "<parameters>",
            f"            <parameters>$(find {name})/config/my_controllers.yaml</parameters>",
        )
        write_lines(ros2_control_path, data)

    shutil.copy(f"{os.path.dirname(__file__)}/files/gazebo_params.yaml", f"{pkg_dir}/config/")
    shutil.copy(f"{os.path.dirname(__file__)}/files/my_controllers.yaml", f"{pkg_dir}/config/")
    shutil.copy(f"{os.path.dirname(__file__)}/files/rsp.launch.py", f"{pkg_dir}/launch/")

    rsp_path = f"{pkg_dir}/launch/rsp.launch.py"
    if os.path.exists(rsp_path):
        data = read_lines(rsp_path)
        insert_after(
            data,
            "def generate_launch_description():",
            f"    pkg_path = os.path.join(get_package_share_directory('{name}'))",
        )
        write_lines(rsp_path, data)

    shutil.copy(f"{os.path.dirname(__file__)}/files/launch_sim.launch.py", f"{pkg_dir}/launch/")

    launch_sim_path = f"{pkg_dir}/launch/launch_sim.launch.py"
    if os.path.exists(launch_sim_path):
        data = read_lines(launch_sim_path)
        insert_after(
            data,
            "def generate_launch_description():",
            f"    package_name='{name}'",
        )
        write_lines(launch_sim_path, data)

    shutil.copy(f"{os.path.dirname(__file__)}/files/empty.world", f"{pkg_dir}/worlds/")


def createMessagePackage(name):
    path = f"{Path(__file__).resolve().parents[1]}/src"
    pkg_dir = f"{path}/{name}"

    safe_rmtree(f"{pkg_dir}/src")
    safe_rmtree(f"{pkg_dir}/include")
    safe_mkdir(f"{pkg_dir}/msg")
    safe_mkdir(f"{pkg_dir}/srv")

    cmake = [
        "cmake_minimum_required(VERSION 3.5)",
        f"project({name})",
        "",
        "# Default to C99",
        "if(NOT CMAKE_C_STANDARD)",
        "    set(CMAKE_C_STANDARD 99)",
        "endif()",
        "",
        "# Default to C++14",
        "if(NOT CMAKE_CXX_STANDARD)",
        "    set(CMAKE_CXX_STANDARD 14)",
        "endif()",
        "",
        'if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")',
        "    add_compile_options(-Wall -Wextra -Wpedantic)",
        "endif()",
        "",
        "# find dependencies",
        "find_package(ament_cmake REQUIRED)",
        "find_package(nav_msgs REQUIRED)",
        "# uncomment the following section in order to fill in",
        "# further dependencies manually.",
        "# find_package(<dependency> REQUIRED)",
        "",
        "if(BUILD_TESTING)",
        "    find_package(ament_lint_auto REQUIRED)",
        "    # the following line skips the linter which checks for copyrights",
        "    # comment the line when a copyright and license is added to all source files",
        "    #set(ament_cmake_copyright_FOUND TRUE)",
        "    # the following line skips cpplint (only works in a git repo)",
        "    # comment the line when this package is in a git repo and when",
        "    # a copyright and license is added to all source files",
        "    #set(ament_cmake_cpplint_FOUND TRUE)",
        "    ament_lint_auto_find_test_dependencies()",
        "endif()",
        "",
        "find_package(rosidl_default_generators REQUIRED)",
        "",
        "rosidl_generate_interfaces(${PROJECT_NAME}",
        '    "msg/Placeholder.msg"',
        '    "srv/Placeholder.srv"',
        ")",
        "",
        "",
        "ament_package()",
    ]
    write_lines(f"{pkg_dir}/CMakeLists.txt", cmake)

    package_xml_path = f"{pkg_dir}/package.xml"
    if os.path.exists(package_xml_path):
        data = read_lines(package_xml_path)
        if "rosidl_default_generators" not in "".join(data):
            insert_before(
                data,
                "</package>",
                [
                    "    <build_depend>rosidl_default_generators</build_depend>",
                    "    <exec_depend>rosidl_default_runtime</exec_depend>",
                    "    <member_of_group>rosidl_interface_packages</member_of_group>",
                ],
            )
            write_lines(package_xml_path, data)

    with open(f"{pkg_dir}/msg/Placeholder.msg", "w", encoding="utf-8", newline="\n") as f:
        f.write("int32 data")

    with open(f"{pkg_dir}/srv/Placeholder.srv", "w", encoding="utf-8", newline="\n") as f:
        f.write("int32 input\n---\nint32 output")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit("Usage: buildNode.py <name> <code> <node>")

    name = sys.argv[1]
    code = sys.argv[2]
    node = sys.argv[3]

    if code == "python":
        createNodePython(name, node)
    elif code == "c++":
        createNodeCpp(name, node)
    elif code == "main":
        createMainPackage(name)
    elif code == "messages":
        createMessagePackage(name)
    else:
        raise SystemExit(f"Unknown code type: {code}")
