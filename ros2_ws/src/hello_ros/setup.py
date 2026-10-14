"""Setuptools metadata used by colcon to build the ROS 2 Python package."""

from setuptools import setup

package_name = "hello_ros"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    py_modules=["hello_pb2", "hello_pb2_grpc"],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/hello_ros"],
        ),
        ("share/hello_ros", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="liya_oz",
    maintainer_email="liya.oz@outlook.com",
    description="A prototype connecting ROS 2 and gRPC.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "hello_publisher = hello_ros.publisher:main",
            "hello_ros = hello_ros.entry_point:main",
        ],
    },
)
