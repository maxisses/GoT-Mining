from flask import Flask, request
from flask_cors import CORS
import time

from transformers import pipeline
import torch
import os

if not os.environ.get("MODELPATH"):
    os.environ["MODELPATH"] = "databricks/dolly-v2-3b"

MODELPATH = os.environ.get("MODELPATH")
print("Model in use from path: " + MODELPATH)

app = Flask(__name__)
CORS(app)

## check GPU availability
if torch.cuda.is_available():
  device = torch.cuda.get_device_name(0)
  print("-------------------")
  print(f'GPU device name: {device}')
  print("-------------------")
else:
  print("-------------------")
  print('No GPU available')
  print("-------------------")

## load ML model
instruct_pipeline = pipeline(model=MODELPATH, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")

@app.route('/')
def generate_response():
    text = request.args.get('text')
    start = time.time()
    response = instruct_pipeline(text)
    print(response)
    # jsonDict = jsonify(response)
    end = time.time()
    elapsed_time = end - start
    print(f"The request took: "+ str(elapsed_time))

    return response, 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
