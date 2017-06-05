# MMSR-Project

docker image with python and opencv3: 
https://hub.docker.com/r/dkarchmervue/python34-opencv3/

to download docker pull dkarchmervue/python34-opencv3

to run with shared volume and shell:
docker run -v /home/liam/git/notflix:/usr/local/notflix  -ti dkarchmervue/python34-opencv3 bash
first the host path then the path in the image
