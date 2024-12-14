'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

ml_modeling.py:
Takes the training data from data_gen.py as a .csv and uses it to train a model to predict if the IP is malicious or benign 

'''

import os
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Construct the path dynamically
base_path = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
data_path = os.path.join(base_path, '../data/geospatial_data.csv')

# Load dataset
dataset = loadtxt(data_path, delimiter=',')

# Split into input (input_field) and output (output_label) variables
input_field = dataset[:, 0:4]
output_label = dataset[:, 4]

# Define the Keras model (No solid reasons for these activations, can try others)
model = Sequential()
model.add(Dense(12, input_shape=(4,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the Keras model (No reason for adam optimizer, can try different ones out to see if they work better)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the Keras model on the dataset
model.fit(input_field, output_label, epochs=150, batch_size=10, verbose=1)

# Evaluate the Keras model
_, accuracy = model.evaluate(input_field, output_label, verbose=0)
print('Accuracy: %.2f' % (accuracy * 100))

# Make predictions
predictions = (model.predict(input_field) > 0.5).astype(int)

# Summarize the first 5 cases
for i in range(5):
    print('Input: %s => Predicted: %d (Expected: %d)' % (input_field[i].tolist(), predictions[i], output_label[i]))
