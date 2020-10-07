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
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
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
              combine=1000,
              batch_size=1,
              model_name='124M',
              steps=1000,
              restore_from='fresh',
              run_name='run1',
              print_every=10,
              sample_every=200,
              save_every=500
              )