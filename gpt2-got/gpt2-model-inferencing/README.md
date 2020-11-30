# gpt-2-cloud-run

Fetch the output of the gpt2-build repo by copying the output into this folder. Create a folder name "checkpoint" and put the output in there. Checkpoint is the folder the gpt2 lib is looking for the output so you have to name it like this.

Build the docker Image with 

docker build -t yourgpt2starter .

Run the docker image 
docker run -p 8080:8080 yourgpt2starter

OR if you have GPUs

docker run -p 8080:8080 --gpus all yourgpt2starter

Depending on your GPU the difference for inferencing is tremendous - for me it was 12x faster with 1 Geforce RTX2080 Super.
The logs show you whether a GPU had been used an how long one request took.

