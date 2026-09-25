import csv
import random

class Reader:
    def __init__(self, filepath):
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)

            self.__columns = next(reader)
            self.__content = []
            for content in reader:
                self.__content.append(content)

    @property
    def columns(self): return self.__columns

    @property
    def content(self): return self.__content

class ml_model:
    '''
        ml_model() class is the main class for generating a offer or checking does user need offer or not.
    '''
    def __init__(self, product_data_filepath='all.csv', user_data_filepath='user.csv'):
        self.products = Reader(product_data_filepath)
        self.users = Reader(user_data_filepath)

    def need_offer(self, user_data):
        '''
            this function is for checking the user data that does him/her need offer or not.
            it checks by the user in_cart / bought_it index in csv data.
            it is optional to checking like this, you can change it to sth like check just by in_cart, it is optional. 
        '''
        if len(list(user_data[::-1][0])) < 1 or len(list(user_data[::-1][1])) < 1: #checks the in_cart and bought_it lengths
            return False #user didn't bought sth or didn't have sth in his/her cart
        return True

    @property
    def rand_user(self):
        '''
            returns one of the users randomly from the csv data of users
        '''
        return random.choice(self.users.content)