'''
CSCI 403 Geospatial Intrusion Detection Project  
By Austin Erickson, Cale Voglewede, and Connor Chandler

geospatial_intrusion.py:
Main runtime function of the geospatial intrusion system, allows each of the 
parts to be run via CLI

'''
import os

def main():

    exit_flag_1 = False
    input_1 = ''
    BASE_PATH = os.path.join(os.path.dirname(__file__), '.')
    os.chdir(BASE_PATH)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('\nCSCI 403 Geospatial Intrusion Detection Project')
    print('By Austin Erickson, Cale Voglewede, and Connor Chandler')

    while(exit_flag_1 == False):
        
        input_1 = input('\n\nPlease press a key then enter to execute a\
 corresponding program module of the geospatial intrusion system:\
         \n\n[a] - Generate Training Data\
           \n[b] - Generate ML Model from Training Data\
           \n[c] - Evaluate IP addresses on ML Model\
           \n[q] - Exit the Program\
           \n\nKey: ')

        if input_1 == 'a':
            exit_flag_2 = False

            while(exit_flag_2 == False):

                input_2 = input('\nEnter how many entries you want (a positive integer): ')
                os.system('python data_gen.py ' + input_2)
                exit_flag_2 = True


        if input_1 == 'b':
            # exec ml_modeling.py
            pass


        if input_1 == 'c':
            exit_flag_4 = False

            while(exit_flag_4 == False):

                input_4 = input('\nEnter a key to choose what source to evaluate:\
                                    \n[a] - Sample IP Addresses\
                                    \n[b] - Input\
                                    \n\nKey: ')
                if input_4 == 'a':
                    os.system('python ip_eval.py 1')
                    exit_flag_4 = True

                if input_4 == 'b':
                    os.system('python ip_eval.py 0')
                    exit_flag_4 = True   


        if (input_1 == 'q'):
            return
            

if __name__ == '__main__':
    main()
