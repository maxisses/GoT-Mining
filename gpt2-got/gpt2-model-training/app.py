import tensorflow as tf
from datetime import datetime
import os
import gpt_2_simple as gpt2
import sys

print("-------------------")
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("-------------------")

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

if len(tf.config.experimental.list_physical_devices('GPU')) == 0:
    print("-------------------")
    print("No GPU found")
    print("-------------------")
else:
    print("-------------------")
    print("GPU found, going on...")
    print("-------------------")

os.system('nvidia-smi')

if os.getenv("MODELSIZE") is None:
  model_size="124M"
else:
  model_size=os.getenv("MODELSIZE")

try:
  os.listdir("models/" + model_size)
  print("-------------------")
  print(f"Model files for {model_size} Model already downloaded")
  print("-------------------")
except:
  gpt2.download_gpt2(model_name=model_size)

file_name = "GoT_textonly.txt"
print("-------------------")
print(f"Using this text file for training: {file_name}")
print("-------------------")

sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset=file_name,
              combine=500,
              batch_size=1,
              model_name='124M',
              accumulate_gradients=5,
              only_train_transformer_layers=True,
              learning_rate=0.0001,
              multi_gpu=True,
              steps=1000,
              restore_from='fresh',
              run_name='run1',
              print_every=10,
              optimizer='adam',
              sample_every=100,
              sample_length=500,
              save_every=500,
              )

gpt2.generate(sess)