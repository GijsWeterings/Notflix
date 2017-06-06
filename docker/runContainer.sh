#!/bin/bash

echo "Make sure to run with sudo"

# Allow Docker access to the X server
# xhost local:root

docker run -v /home/gijs/Projects/TUDelft/MMSR-Project/videos:/videos -v /tmp/.X11-unix:/tmp/.X11-unix --privileged -it opencv3

