'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

ip_data.py:
Classifies fields from ip-api's API into a class

'''

class IP_Data:

    def __init__(self, n1=0, n2=0, n3=0, n4=0):

        self.is_proxy = bool(n1)
        # corresponds to proxy field
        
        self.in_NA = bool(n2)
        # corresponds to continentCode field, NA = North America
        
        self.in_US = bool(n3)
        # corresponds to countryCode field, US = United States
        
        self.in_ND_or_MN = bool(n4)
        # corresponds to region field, ND = North Dakota, MN = Minnesota


    def __str__(self):
        return('Is Proxy: ' + str(self.is_proxy) + ' \n'
            +  'In North America: ' + str(self.in_NA) + ' \n'
            +  'In United States: ' + str(self.in_US) + ' \n'
            +  'In North Dakota or Minnesota: ' + str(self.in_ND_or_MN) + ' \n')

    
    def set_proxy(boolean):
        if not (isinstance(boolean, bool)):
            raise Exception('Not of bool type')
        else:
            self.is_proxy = boolean


    def set_in_NA(boolean):
        if not (isinstance(boolean, bool)):
            raise Exception('Not of bool type')
        else:
            self.in_NA = boolean


    def set_in_US(boolean):
        if not (isinstance(boolean, bool)):
            raise Exception('Not of bool type')
        else:
            self.in_US = boolean


    def set_in_ND_or_MN(boolean):
        if not (isinstance(boolean, bool)):
            raise Exception('Not of bool type')
        else:
            self.in_ND_or_MN = boolean

    
        

    