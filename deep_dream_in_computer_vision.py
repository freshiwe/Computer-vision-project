# -*- coding: utf-8 -*-
"""Deep dream in Computer Vision.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KUYMx_bFYlV58VXLirEZUAeq4Ytuu4xB

# Computer Vision Masterclass: Deep Dream

## Importing the libraries

- Adapted from: https://www.tensorflow.org/beta/tutorials/generative/deepdream
"""

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
tf.__version__

"""## Loading the pre-built convolutional neural network

- InceptionNet: https://www.tensorflow.org/api_docs/python/tf/keras/applications/inception_v3
- Original paper: https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Szegedy_Rethinking_the_Inception_CVPR_2016_paper.pdf
- Imagenet: http://www.image-net.org/
"""

base_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')

base_model.summary()

len(base_model.layers)

# Relu
#names = ['mixed3', 'mixed5', 'mixed8', 'mixed9']
names = ['mixed3', 'mixed5']

base_model.input

layers = [base_model.get_layer(name).output for name in names]

layers

deep_dream_model = tf.keras.Model(inputs = base_model.input, outputs = layers)

"""## Loading and pre-processing the image"""

from google.colab import drive
drive.mount('/content/drive')

image = tf.keras.preprocessing.image.load_img('/content/drive/.shortcut-targets-by-id/1fnn6e8q7Ykp7nqOPWGeSiijlNTt_kkPL/Computer Vision Masterclass/Images/StaryNight.jpg',
                                              target_size=(225, 375))

plt.imshow(image);

type(image)

image.size

image.mode, len(image.mode)

list(image.getdata())

image = tf.keras.preprocessing.image.img_to_array(image)

type(image)

image.shape

image.min(), image.max()

# image = image / 255
image = tf.keras.applications.inception_v3.preprocess_input(image)

image.min(), image.max()

"""## Getting the activations"""

image.shape

image_batch = tf.expand_dims(image, axis = 0)

image_batch.shape

activations = deep_dream_model.predict(image_batch)

deep_dream_model.outputs

len(activations)

activations[1]

activations[0].shape, activations[1].shape

"""## Calculating the loss"""

def calculate_loss(image, network):
  image_batch = tf.expand_dims(image, axis = 0)
  activations = network(image_batch)

  losses = []
  for act in activations:
    loss = tf.math.reduce_mean(act)
    losses.append(loss)

  #print(losses)
  #print(np.shape(losses))
  #print(tf.reduce_sum(losses))

  return tf.reduce_sum(losses)

0.45195404 + 0.16485049

loss = calculate_loss(image, deep_dream_model)
loss

"""## Gradient ascent"""

# Compare the activations with the pixels
# Emphasize parts of the image
# Change the pixels of the input image

@tf.function
def deep_dream(network, image, learning_rate):
  with tf.GradientTape() as tape:
    tape.watch(image)
    loss = calculate_loss(image, network)

  gradients = tape.gradient(loss, image) # Derivate
  gradients /= tf.math.reduce_std(gradients)
  image = image + gradients * learning_rate
  image = tf.clip_by_value(image, -1, 1)

  return loss, image

def inverse_transform(image):
  image = 255 * (image + 1.0) / 2.0
  return tf.cast(image, tf.uint8)

def run_deep_dream(network, image, epochs, learning_rate):
  for epoch in range(epochs):
    loss, image = deep_dream(network, image, learning_rate)

    if epoch % 200 == 0:
      plt.figure(figsize=(12,12))
      plt.imshow(inverse_transform(image))
      plt.show()
      print('Epoch {}, loss {}'.format(epoch, loss))

"""## Generating images"""

image.shape, type(image)

run_deep_dream(network=deep_dream_model, image=image, epochs = 8000, learning_rate=0.0001)

"""## Homework"""

image = tf.keras.preprocessing.image.load_img('/content/drive/MyDrive/Cursos - recursos/Computer Vision Masterclass/Images/sky.jpeg',
                                              target_size = (225, 375))

plt.imshow(image);

image = tf.keras.preprocessing.image.img_to_array(image)
image = tf.keras.applications.inception_v3.preprocess_input(image)

run_deep_dream(network = deep_dream_model, image = image, epochs = 8000, learning_rate = 0.0001)