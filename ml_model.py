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
    def __init__(self, product_data_filepath='all.csv', user_data_filepath='user.csv'):
        self.products = Reader(product_data_filepath)
        self.users = Reader(user_data_filepath)

    @property
    def rand_user(self): return random.choice(self.users.content)