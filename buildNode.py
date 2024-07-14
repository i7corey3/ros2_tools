import os
import sys
import yaml
from pathlib import Path


def camel_case(s):
    newString = ''
    temp = s.split('_')
    for st in temp:
        newString += (st[0].upper() + st[1:])
    return newString
    
def createNodePython(name, node):
    path = f"{Path(__file__).parents[1]}/src"
   
    with open(f"{path}/{name}/{name}/{name}.py", "w") as file:

        data = ["import rclpy",
                "from rclpy.node import Node",
                "import time",
                " ",
                " ",
                f"class {camel_case(name)}(Node):",
                "\tdef __init__(self):",
                f"\t\tsuper().__init__('{node}')",
                '',
                "\t\tself.declare_parameters(",
                '\t\t\tnamespace="",',
                '\t\t\tparameters=[',
                '',
                '\t\t\t]',
                '\t\t)',
                " ",
                '\t\tself.sim_time = self.get_parameter("use_sim_time").get_parameter_value().bool_value',
                '',
                '\t\tself.get_logger().info(f"sim_time is set to {self.sim_time}")',
                '',
                "\ttime.sleep(1)",
                " ",
                " ",
                " ",
                "def main(args=None):",
                "   rclpy.init(args=args)",
                " ",
                f"   {name} = {camel_case(name)}()",
                " ",
                f"   rate = {name}.create_rate(20)",
                "   while rclpy.ok():",
                f"      rclpy.spin_once({name})",
                "",
                f"   {name}.destroy_node()",
                "   rclpy.shutdown()"
                
                ]

        for line in data:
           file.write(line + '\n')


   

    with open(f"{path}/{name}/setup.py", "r") as f:
        data = f.readlines()

    data.insert(1, "import os\n")
    data.insert(2, "from glob import glob\n")
    data.insert(14, "\t\t(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),\n")
    data.insert(15, "\t\t(os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*[yaml]*'))),\n")
    data.insert(26, f"\t\t\t'{node} = {name}.{name}:main'\n")

    s = ""
    for i in data:
        s += i

    os.remove(f"{path}/{name}/setup.py")

    with open(f"{path}/{name}/setup.py", "w") as f:
        f.write(s)
    
    os.mkdir(f"{path}/{name}/config")
    os.mkdir(f"{path}/{name}/launch")

    with open(f"{path}/{name}/config/params.yaml", "w") as f:
        data = [{f"{node}": {'ros__parameters': {'use_sim_time': False}}}]
        yaml.dump_all(data, f)

    with open(f"{path}/{name}/launch/{name}.launch.py", "w") as f:
        
        data = [
            "import os",
            " ",
            "from ament_index_python.packages import get_package_share_directory",
            "from launch.substitutions import LaunchConfiguration",
            "from launch.actions import DeclareLaunchArgument",
            "from launch import LaunchDescription",
            "from launch_ros.actions import Node",
            "from pathlib import Path",
            " ",
            " ",
            "def generate_launch_description():",
            " ",
                f"\tpackage_name = '{name}'\n",
            " ",
            "\tparams_file = os.path.join(get_package_share_directory(package_name), 'config', 'params.yaml')",
            "\tcwd = f'{Path(__file__).parents[5]}/src/{package_name}/config/params.yaml'",
	        "\tos.system(f'cp {cwd} {params_file}')",
            " ",
            f"\t{name} = Node(",
            "\t\tpackage=package_name,",
            f"\t\texecutable='{node}',",
            "\t\tparameters=[params_file]",
            " ",
            "\t)",
            " ",
            "\treturn LaunchDescription([",
            f"\t\t{name}",
            "\t])"
        ]

        for line in data:
           f.write(line + '\n')

def createNodeCpp(name, node):
    path = f"{Path(__file__).parents[1]}/src"
    with open(f"{path}/{name}/src/{name}.cpp", "w") as file:

        data = [
            "#include <iostream>",
            "#include <chrono>",
            "#include <functional>",
            "#include <memory>",
            "#include <string>",
            "#include <vector>",
            "#include <ament_index_cpp/get_package_share_directory.hpp>",
            " ",
            " ",
            '#include "rclcpp/rclcpp.hpp"',
            " ",
            "using namespace std::chrono_literals;",
            " ",
            f"class {camel_case(name)} : public rclcpp::Node",
            "{",
            " ",
            f"    public:",
            f"       {camel_case(name)}()",
            f'        : Node("{node}")',
            f"        {'{ }'}",
            " ",
            " ",
            "};",
            " ",
            " ",
            "int main(int argc, char * argv[])",
            "{",
            f"    rclcpp::init(argc, argv);",
            f"    rclcpp::spin(std::make_shared<{camel_case(name)}>());",
            f"    rclcpp::shutdown();",
            " ",
            f"    return 0;",
            "}",
        ]

        for line in data:
           file.write(line + '\n')

    
    with open(f"{path}/{name}/CMakeLists.txt", "r") as f:
        data = f.readlines()

    data.insert(9, "find_package(rclcpp REQUIRED)\n")
    data.insert(10, "find_package(std_msgs REQUIRED)\n")
    data.insert(26, "include_directories(include)\n")
    
    lines = [
        " ",
        "set(dependencies",
        "\trclcpp",
        "\tstd_msgs",
        ")",
        " ",
        "## COMPILE",
        "add_library(",
        "\t${PROJECT_NAME}",
        "\tSHARED",
        f"\tsrc/{name}.cpp",
        ")",
        " ",
        "target_include_directories(",
        "\t${PROJECT_NAME}",
        "\tPRIVATE",
        "\tinclude",
        ")",
        " ",
        "ament_target_dependencies(",
        "\t${PROJECT_NAME}",
        "\tPUBLIC",
        "\t${dependencies}",
        " ",
        ")",
        " ",
        "add_executable(",
        f"\t{node}",
        f"\tsrc/{name}.cpp",
        ")",
        " ",
        f"ament_target_dependencies({node} ${'{dependencies}'})",
        " ",
        "install(",
        "\tTARGETS", 
        "\t${PROJECT_NAME}",
        "\tDESTINATION lib/${PROJECT_NAME}",
        ")",
        " ",
        "# INSTALL",
        "install(",
        "\tTARGETS ",
        f"\t{node}",
        "\tDESTINATION lib/${PROJECT_NAME}",
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
        "\tinclude",
        ")",
        " ",
        "ament_export_libraries(",
        "\t${PROJECT_NAME}",
        ")",
        " ",
        "\tament_export_dependencies(",
        "\t${dependencies}",
        ")",
        " ",
        " ",
        "ament_export_include_directories(include)"
    ]
    ss = ""
    for i in lines:
        ss = ss + i + "\n"
    data.insert(27, ss)

    s = ""
    for i in data:
        s += i

    os.remove(f"{path}/{name}/CMakeLists.txt")

    with open(f"{path}/{name}/CMakeLists.txt", "w") as f:
        f.write(s)
    
    os.mkdir(f"{path}/{name}/config")
    os.mkdir(f"{path}/{name}/launch")

    with open(f"{path}/{name}/config/params.yaml", "w") as f:
        data = [{f"{node}": {'ros__parameters': {'use_sim_time': False}}}]
        yaml.dump_all(data, f)

    with open(f"{path}/{name}/launch/{name}.launch.py", "w") as f:
        
        data = [
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
                f"\tpackage_name = '{name}'\n",
            " ",
            "\tparams_file = os.path.join(get_package_share_directory(package_name), 'config', 'params.yaml')",
            " ",
            f"\t{name} = Node(",
            "\t\tpackage=package_name,",
            f"\t\texecutable='{node}',",
            "\t\tparameters=[params_file]",
            " ",
            "\t)",
            " ",
            "\treturn LaunchDescription([",
            f"\t\t{name}",
            "\t])"

        ]

        for line in data:
           f.write(line + '\n')


if __name__ == '__main__':
    
    name = sys.argv[1]
    code = sys.argv[2]
    node = sys.argv[3]
    if code == "python":
        createNodePython(name, node)
    elif code == "c++":
        createNodeCpp(name, node)
