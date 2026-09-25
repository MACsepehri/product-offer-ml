import csv
import random
from sklearn.linear_model import LinearRegression


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
        self.L_model = LinearRegression()
        self.L_sample_offer_model = LinearRegression()
        self.__is_fitted = False

    def __parse_list(self, raw):
        '''
            '['a', 'b']' -> 2
        '''
        raw = raw.strip()
        if raw in ('', '[]'):
            return 0
        return raw.count("'") // 2

    def fit_data(self):
        '''
            start adding data.
        '''
        X = []
        y = []

        cols = self.users.columns
        i_discount = cols.index('discount_percent')
        i_in_cart = cols.index('in_cart')
        i_bought = cols.index('bought_it')

        for row in self.users.content:
            if len(row) < len(cols):
                continue

            try:
                discount = float(row[i_discount])
                in_cart = self.__parse_list(row[i_in_cart])
                bought = self.__parse_list(row[i_bought])
            except ValueError:
                continue

            score = min(10.0, max(1.0, in_cart * 1.5 + bought * 1.0 + discount * 0.1))

            X.append([in_cart, bought, discount])
            y.append(score)

        if not X:
            raise ValueError('The uesr dataset is invalid.')

        self.L_sample_offer_model.fit(X, y)
        self.__is_fitted = True
        return self.L_sample_offer_model

    def need_offer(self, user_data, has_offer=1):
        '''
            give you the predicted score if we give user offer or not
        '''
        if not self.__is_fitted:
            raise RuntimeError("Model is not fitted. Call fit_data() first.")

        if len(user_data) < 3:
            raise ValueError("user_data must have in_cart, bought and discount indexes")

        in_cart, bought, discount = float(user_data[0]), float(user_data[1]), float(user_data[2])
        X = [[in_cart, bought, discount]]

        raw = self.L_sample_offer_model.predict(X)[0]

        return max(1.0, min(10.0, raw))

    @property
    def rand_user(self):
        '''
            returns one of the users randomly from the csv data of users
        '''
        cols = self.users.columns
        i_discount = cols.index('discount_percent')
        i_in_cart = cols.index('in_cart')
        i_bought = cols.index('bought_it')

        row = random.choice(self.users.content)
        return [
            self.__parse_list(row[i_in_cart]),
            self.__parse_list(row[i_bought]),
            float(row[i_discount]),
        ]