#!/bin/bash -xve

#sync and make
#Copy repositories to workspace
rsync -av ./ ~/catkin_ws/src/pimouse_run_corridor/

#bring pimouse_ros to workspace by git clone
cd ~/catkin_ws/src
git clone --depth=1 https://github.com/AIT-doki-robot/pimouse_ros.git
cd ~/catkin_ws
catkin_make
source ~/.bashrc
