'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

data_gen.py:
Generates fake data to be modeled for geospatial detection

'''

import os
import sys
import secrets
import random
import math
from enum import Enum

TRAINING_DATA_FILE = '../data/geospatial_data.csv'


def training_data_file_exists():
    return os.path.exists(TRAINING_DATA_FILE)


def data_check():

    if training_data_file_exists() == False:
        file = open(TRAINING_DATA_FILE, 'x')
        file.close()
        return False
        
    return True


def generate_data(num_of_entries):
    '''
    Data about an IP is represented by 5 bits.
    Each bit is an attribute about the IP.
    The following indicates what each bit means.

    (from left to right, describes if bit is active)
    1st Bit - IP address marked as a proxy, VPN, etc.
    2nd Bit - IP address marked as being in North America
    3rd Bit - IP address marked as being in the United States
    4th Bit - IP address marked as being in North Dakota or Minnesota
    5th Bit - IP address marked as being illegitimate, for ML labeling

    IP addresses marked as a proxy are never considered legitimate
    due to trying to subvert geospatial analysis.
    '''

    if not (isinstance(num_of_entries, int)):
        raise Exception('Not of int type')

    if data_check() == True:

        file = open(TRAINING_DATA_FILE, 'a')

        for entry in range(math.ceil(num_of_entries/2)):
        # for IP addresses to be considered illegitimate

            chances_1 = generate_random_reference(proxy_chances)

            if secrets.choice(chances_1) == ('PROXY'):
                
                chances_2 = generate_random_reference(geo_data_proxy_chances)
                selection = secrets.choice(chances_2)

                if selection  == ('INTL_PROXY'):
                    file.write("1,0,0,0,1\n")

                if selection == ('NA_PROXY'):
                    file.write("1,1,0,0,1\n")

                if selection == ('US_PROXY'):
                    file.write("1,1,1,0,1\n")

                if selection == ('ND_OR_MN_PROXY'):
                    file.write("1,1,1,1,1\n")


            else:

                chances_2 = generate_random_reference(geo_data_not_proxy_chances)
                selection = secrets.choice(chances_2)

                if selection == ('INTL'):
                    file.write("0,0,0,0,1\n")

                if selection == ('NA'):
                    file.write("0,1,0,0,1\n")

                if selection == ('US'):
                    file.write("0,1,1,0,1\n")

                if selection == ('ND_OR_MN'):
                    file.write("0,1,1,1,1\n")


        for entry in range(math.floor(num_of_entries/2)):
        # for IP addresses to be considered legitimate

                chances = generate_random_reference(geo_data_legitimate_chances)
                selection = secrets.choice(chances)

                if selection == ('INTL'):
                    file.write("0,0,0,0,0\n")

                if selection == ('NA'):
                    file.write("0,1,0,0,0\n")

                if selection == ('US'):
                    file.write("0,1,1,0,0\n")

                if selection == ('ND_OR_MN'):
                    file.write("0,1,1,1,0\n")


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
    PROXY = 30
    NOT_PROXY = 70


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

class geo_data_legitimate_chances(Enum):
    INTL = 1
    NA = 4
    US = 10
    ND_OR_MN = 85

if __name__ == "__main__":
    num_of_entries = int(sys.argv[1])
    generate_data(num_of_entries)