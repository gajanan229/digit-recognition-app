# -*- coding: utf-8 -*-
"""digit_recognition_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N6ADKO7KBSZx1qCus-UDvICjmei89Ipv

## Importing Libraries


```
# This is formatted as code
```
"""

import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.activations import linear, relu, sigmoid
import tensorflow as tf

"""## Import Data

"""

from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

"""Prepping Data"""

# Reshaping the input data
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
# Encoding the labels
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)
# Data type conversion and normalization
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

"""## Defining and Training The Model"""

# Define the model
model = Sequential([
    Flatten(input_shape=(28, 28, 1)),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(10, activation='linear')
])

model.summary()

# Compile the model
model.compile(
              optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=12, batch_size=32, validation_split=0.2)

"""## Testing and Saving The Model"""

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test Accuracy:", test_acc)

# Predict labels for test data
predictions = model.predict(x_test)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = np.argmax(y_test, axis=1)

# Count the number of mistakes
num_mistakes = np.sum(predicted_labels != true_labels)
print("Number of mistakes:", num_mistakes)

model.save("mnist_model.h5")