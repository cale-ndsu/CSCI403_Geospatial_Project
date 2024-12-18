'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

ip_eval.py:
Evaluates and returns data about an IP address from ip-api 

ip_api's website: https://ip-api.com/
'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import sys
import requests
import json
import socket
import ipaddress
import time
from ip_data import IP_Data
import numpy
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

BASE_PATH = os.path.dirname(os.path.abspath(__file__))  
COMPILED_MODEL_PATH = os.path.join(BASE_PATH, '../data/ml_model.h5')
SAMPLE_DATA_PATH = os.path.join(BASE_PATH, '../data/sample_ip_addresses.txt')


def eval_main(an_input):
    option = ''
    try:
        option = int(an_input)
    except:
        return

    if option == 1: # evaluate all IP addresses in a .txt file

        model_path = os.path.join(BASE_PATH, '../data/ml_model.h5')
        if not os.path.exists(model_path):
            raise Exception(f'Model file not found at {model_path}. Train the model first.')

        model = tensorflow.keras.models.load_model(model_path)
        
        # Recompile model with no metrics for inference
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[])

        if not sample_ip_addresses_exist():
            raise Exception('Could not find data at ../data/sample_ip_addresses.txt')

        with open(SAMPLE_DATA_PATH,'r') as file:
            lines = file.readlines()
            for ip in lines:
                ip = ip.replace("\n","")
                evaluate(ip,model)

    elif option == 0: # evaluate an IP address from user input
        exit_flag = False

        model_path = os.path.join(BASE_PATH, '../data/ml_model.h5')
        if not os.path.exists(model_path):
            raise Exception(f'Model file not found at {model_path}. Train the model first.')

        model = tensorflow.keras.models.load_model(model_path)
        
        # Recompile model with no metrics for inference
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[])

        while(exit_flag == False):
            ip_input = input("\nPlease enter a valid IP address: ")

            if valid_ipv4(ip_input) == True or valid_ipv6(ip_input) == True:
                evaluate(ip_input,model)
                exit_flag = True

    else:
        return

# Pass in IP and model so that the model isnt compiled every loop
def evaluate(ip_address,model):

    json = get_json(ip_address)

    ip_continent_code = json['continentCode']
    ip_country = json['country']
    ip_country_code = json['countryCode']
    ip_region = json['region']
    ip_region_name = json['regionName']
    ip_city = json['city']
    ip_isp = json['isp']
    ip_proxy = json['proxy']

    # print information about IP
    print('\nInformation about %s\n---------------------------------\
            \n%s  %s, %s  %s\n%9s  %s' \
            % (ip_address,'Location:',ip_city, \
            ip_region_name,ip_country,'ISP:',ip_isp))
    time.sleep(3)

    encoded_data = \
     map_json_to_data_and_class(ip_proxy,ip_continent_code,ip_country_code,ip_region)

    # print encoding of IP
    print('\n\n %s as Encoded Data\n---------------------------------\
            \n%12s\n%12s%d,%d,%d,%d\n%12s-------\n%s' % (ip_address, ' ', ' ', \
            encoded_data[0],encoded_data[1],encoded_data[2], \
            encoded_data[3], ' ', str(encoded_data[4])))
    time.sleep(3)

    print('\nEvaluating %s on machine learning model...\n' % (ip_address))
    time.sleep(3)

    # Prepare data for prediction
    input_data = numpy.array(encoded_data[:4]).reshape(1, -1)  # Convert to 2D NumPy array for prediction

    # Make prediction
    prediction = model.predict(input_data)[0][0]  # Get the predicted probability

    # Interpret prediction
    if prediction > 0.5:
        print(f'\nPrediction: {ip_address} should be BLOCKED (malicious, confidence: {prediction:.2f})\n')
    else:
        print(f'\nPrediction: {ip_address} is SAFE (benign, confidence: {prediction:.2f})\n')


def get_json(ip_address):

    web_address = 'http://ip-api.com/json/' + ip_address + '?fields=3338239'
    # fields=3338239 gets the various fields that we might want to print out / use from API
    request = requests.get(web_address)
    json = request.json()
    if json['status'] == 'fail':
        raise Exception('Unsuccessful API call. Make sure IP address is written correctly.')
    return json


def map_json_to_data_and_class(ip_proxy,ip_continent_code,ip_country_code,ip_region):

    data = []

    if ip_proxy == True:
        data.append(1)
    else:
        data.append(0)

    if ip_continent_code == 'NA':
        data.append(1)
    else:
        data.append(0)
    
    if ip_country_code == 'US':
        data.append(1)
    else:
        data.append(0)

    if ip_region == 'ND' or ip_region == 'MN':
        data.append(1)
    else:
        data.append(0)

    ip_class = IP_Data(data[0],data[1],data[2],data[3])
    data.append(ip_class)

    return data


def sample_ip_addresses_exist():
    return os.path.exists(SAMPLE_DATA_PATH)


def valid_ipv4(ip_address):
    try: 
        ipaddress.IPv4Address(ip_address)
        return True
    except:
        return False

def valid_ipv6(ip_address):
    try: 
        ipaddress.IPv6Address(ip_address)
        return True
    except:
        return False


if __name__ == '__main__':
    eval_main(sys.argv[1])
