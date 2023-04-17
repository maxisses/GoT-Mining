# Game of Thrones text generator based on GPT2
Clone the repo, build the docker image:
docker build --file Dockerfile-GPU -t gpt2trainmodel:gpu .
docker build --file Dockerfile-CPU -t gpt2trainmodel:cpu . 

and run it with mount of the "checkpoint" folder of the container to your disk.

docker run -v $PWD/checkpoint:/checkpoint gpt2trainmodel:cpu
 
Thats where the model will be put.

The container is based on tensorflow-gpu==1.15.0 so you can it with gpus enabled:
docker run --gpus all -v $PWD/checkpoint:/checkpoint gpt2trainmodel:gpu
