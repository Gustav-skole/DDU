from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import pandas as pd

import glob, pathlib

data_dir = pathlib.Path("DATA")

train_images = list(data_dir.glob('train/*'))
train_labels = pd.read_csv("DATA/train.csv")
#input:
# RGB billeder 72px x 72px x 3 kanaler, 72x72x3 matrix
#output:
# (x1,y1 ... x8,y8), 1x16 matrix

model = models.Sequential()
model.add(layers.Conv2D(32, (6,6), activation='relu', input_shape=(72,72,3)))
model.add(layers.MaxPooling2D((4,4)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(
	optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy']
	)

history = model.fit(train_images, train_labels,steps_per_epoch=16, epochs=10, validation_data=(test_images, test_labels))

plt.plot(history.history['accuracy'], label="accuracy")
plt.plot(history.history['val_accuracy'], label="val_accuracy")
plt.ylim([0.5,1])
plt.legend(loc="lower right")

test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print("Loss: " + str(test_loss))
print("Accuracy: " + str(test_accuracy))