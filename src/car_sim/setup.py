from setuptools import setup
import os
from glob import glob

package_name = 'car_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'world'), glob('world/*.sdf')),  
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')), 

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='haiyunning',
    maintainer_email='haiyunning@gmx.com',
    description='ROS 2 car simulation package using Gazebo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Add Python nodes here if needed later
            'spawn_car = car_sim.spawn_car:main',
        ],
    },
)
