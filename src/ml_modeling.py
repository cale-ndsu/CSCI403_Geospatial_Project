'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

ml_modeling.py:
Takes the training data from data_gen.py as a .csv and uses it to train a model to predict if the IP is malicious or benign 

'''

import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

# Load and preprocess data
def load_data(file_path):
    dataset = np.loadtxt(file_path, delimiter=',')
    X = dataset[:, 0:4]  # Input features
    y = dataset[:, 4]    # Output labels
    return X, y


# Define and compile the Keras model
def build_and_compile_model(input_dim):
    model = Sequential()
    model.add(Dense(12, input_shape=(input_dim,), activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


# Train the model
def train_model(model, X, y, epochs=150, batch_size=10):
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)


# Save the trained model to an H5 file
def save_model(model, file_path):
    model.save(file_path)
    print(f"Model saved to {file_path}")


# Load a pre-trained model from an H5 file
def load_trained_model(file_path):
    if os.path.exists(file_path):
        model = load_model(file_path)
        print(f"Model loaded from {file_path}")
        return model
    else:
        raise FileNotFoundError(f"Model file {file_path} not found.")
    
    # Evaluate the model on a dataset
def evaluate_model(model, X, y):
    _, accuracy = model.evaluate(X, y, verbose=0)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    return accuracy


# Main program loop
def main_ml():
    # File paths
    data_file_path = '../data/geospatial_data.csv'
    model_file_path = '../data/ml_model.h5'

    # Load the data
    X, y = load_data(data_file_path)

    # Check if a saved model exists
    if os.path.exists(model_file_path):
        # Load the pre-trained model
        
        model = load_trained_model(model_file_path)
    else:
        # Build, train, and save a new model
        model = build_and_compile_model(X.shape[1])
        train_model(model, X, y, epochs=150, batch_size=10)
        save_model(model, model_file_path)


if __name__ == "__main__":
    main_ml()
