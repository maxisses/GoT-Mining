# gpt2-model-inferencing


Build the docker Image with 

docker build -t gpt2inferencing .

Run the docker image 
docker run -p 8080:8080 gpt2inferencing

OR if you have GPUs

docker run -p 8080:8080 --gpus all gpt2inferencing

Depending on your GPU the difference for inferencing is tremendous - for me it was 12x faster with 1 Geforce RTX2080 Super.
The logs show you whether a GPU had been used an how long one request took.

