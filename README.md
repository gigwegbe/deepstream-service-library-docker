# Deepstream Service Library Docker
The repo contains  docker setup for Deepstream Service Library 


### Install system dependencies
To run the project, first run the `docker_setup.sh` to install all necessary system dependencies. 
~~~
chmod +x *.sh
~~~
~~~
./docker_setup.sh
~~~
 
### Build a container
To run the inference, you need to first create a docker container with all the requirements. 
- First, build the docker image: 
```bash
docker build -t dslv1 . 
```
- Create a docker container:
~~~
./docker_run.sh
~~~
- Run the example script in `/deepstream-service-library-docker/examples/python` directory:
~~~
 python3 player_play_all_mp4_files_found.py
~~~
