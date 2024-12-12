'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

data_gen.py:
Generates fake data to be modeled for the Geospatial Detection

'''

import os
import sys
import secrets
import random
from enum import Enum

TRAINING_DATA_FILE = '../data/geospatial_data_malicious_ip.csv'


def training_data_file_exists():
    return os.path.exists(TRAINING_DATA_FILE)


def data_check():

    if training_data_file_exists() == False:
        file = open(TRAINING_DATA_FILE, 'x')
        file.close()
        return False
        
    return True


def generate_data(num_of_entries):

    if not (isinstance(num_of_entries, int)):
        raise Exception('Not of int type')

    if data_check() == True:

        file = open(TRAINING_DATA_FILE, 'a')

        for entry in range(num_of_entries):

            chances_1 = generate_random_reference(proxy_chances)

            if secrets.choice(chances_1) == ('PROXY'):
                
                chances_2 = generate_random_reference(geo_data_proxy_chances)
                selection = secrets.choice(chances_2)

                if selection  == ('INTL_PROXY'):
                    file.write("1,0,0,0\n")

                if selection == ('NA_PROXY'):
                    file.write("1,1,0,0\n")

                if selection == ('US_PROXY'):
                    file.write("1,1,1,0\n")

                if selection == ('ND_OR_MN_PROXY'):
                    file.write("1,1,1,1\n")


            else:

                chances_2 = generate_random_reference(geo_data_not_proxy_chances)
                selection = secrets.choice(chances_2)

                if selection == ('INTL'):
                    file.write("0,0,0,0\n")

                if selection == ('NA'):
                    file.write("0,1,0,0\n")

                if selection == ('US'):
                    file.write("0,1,1,0\n")

                if selection == ('ND_OR_MN'):
                    file.write("0,1,1,1\n")


        file.close()

    else:
        raise Exception('Data file did not exist. Make sure file exists under data folder.')


def generate_random_reference(Enum):
    
    chance = []
    for item in Enum:
        for entry in range(item.value):
            chance.append(item.name)

    random.shuffle(chance)

    return chance


class proxy_chances(Enum):
    PROXY = 40
    NOT_PROXY = 60


class geo_data_proxy_chances(Enum):
    INTL_PROXY = 30
    NA_PROXY = 10
    US_PROXY = 35
    ND_OR_MN_PROXY = 25


class geo_data_not_proxy_chances(Enum):
    INTL = 50
    NA = 20
    US = 28
    ND_OR_MN = 2

