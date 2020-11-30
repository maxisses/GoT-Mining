# Game of Thrones text generator based on GPT2
Clone the repo, build the docker image:
docker build --file Dockerfile-GPU -t gpugpt2builder .
docker build --file Dockerfile-CPU -t cpugpt2builder . 

and run it with mount of the "checkpoint" folder of the container to your disk.

docker run -v $PWD/checkpoint:/checkpoint cpugpt2builder
 
Thats where the model will be put.

The container is based on tensorflow-gpu==1.15.0 so you can it with gpus enabled:
docker run --gpus all -v $PWD/checkpoint:/checkpoint gpugpt2builder
