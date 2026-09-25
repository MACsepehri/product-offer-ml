import csv
import random
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


class Response:
    def __init__(self, product, similarity_score, offer_score, user_data, offer):
        self.data = (product,similarity_score,offer_score,user_data,offer)
    
    @property
    def product(self): return self.data[0]
    @property
    def similarity_score(self): return self.data[1]
    @property
    def offer_score(self): return self.data[2]
    @property
    def user_data(self): return self.data[3]
    @property
    def offer(self): return self.data[4]


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

        # creating some base vars for handle finding the most similar products.
        self.__tfidf = TfidfVectorizer()
        self.__tfidf_matrix = None
        self.__product_texts = None

    def __build_tfidf(self):
        '''
            creating TF-IDF matrix for products (just once)
        '''
        if self.__tfidf_matrix is not None:
            return

        cols = self.products.columns

        i_brand = cols.index('brand') if 'brand' in cols else None
        i_name  = cols.index('name')  if 'name'  in cols else None

        texts = []
        for row in self.products.content:
            brand = row[i_brand] if i_brand is not None and i_brand < len(row) else ''
            name  = row[i_name]  if i_name  is not None and i_name  < len(row) else ''

            texts.append(f"{brand} {name}".strip())

        self.__product_texts = texts
        self.__tfidf_matrix = self.__tfidf.fit_transform(texts)

    def __extract_user_brands(self, user_row):
        '''
            getting brands.
        '''
        bought_products = user_row[7].split(';')
        base_brand = [b.replace('"', '') for b in bought_products]
        brands = [
            brand.split('-')[0].replace('[', '').replace(']', '')
                 .replace("'", '').replace(' ', '')
            for brand in base_brand
        ]
        return [b for b in brands if b]

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
        i_discount = cols.index('total_products_discount_percent')
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

    def predict_offer_score(self, user_data, has_offer=1):
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
    
    def predict(self, user_data):
        '''
            returns variety results:
            - offer for example 50% offer
            - returns a product that is similar to bought/cart products
        '''
        if not user_data:
            raise ValueError('Not valid user data.')
        if not self.__is_fitted:
            raise RuntimeError("Model is not fitted. Call fit_data() first.")
        if (user_data[0][0]) < 1 and (user_data[0][1]) < 1:
            return 'User didn`t buy anything or add anything to his/her cart.'

        # starting tfidf and getting brands
        self.__build_tfidf()

        brands = self.__extract_user_brands(user_data[1])
        if not brands:
            return 'No similar product found.'

        user_query = ' '.join(brands)
        user_vec = self.__tfidf.transform([user_query])

        # finding the best product
        sims = cosine_similarity(user_vec, self.__tfidf_matrix).flatten()

        best_idx = int(sims.argmax())
        best_score = float(sims[best_idx])

        # if the score was very low, the product isn't very similar.
        if best_score < 0.05:
            return 'No similar product found.'

        cols = self.products.columns
        best_row = self.products.content[best_idx]
        best_product = dict(zip(cols, best_row))

        # offer score
        score_result = self.predict_offer_score(user_data[0])

        return Response(
            best_product,
            round(best_score, 4),
            round(score_result, 4),
            user_data,
            f'{int(score_result*5)}%'
        )

    @property
    def rand_user(self):
        '''
            returns one of the users randomly.
            index 1 :
                in-cart , bought-it , total-discount (all of them are total)
            index 2 :
                all-data-of-user
        '''
        cols = self.users.columns
        i_discount = cols.index('total_products_discount_percent')
        i_in_cart = cols.index('in_cart')
        i_bought = cols.index('bought_it')

        row = random.choice(self.users.content)
        return [
            [
                self.__parse_list(row[i_in_cart]),
                self.__parse_list(row[i_bought]),
                float(row[i_discount]),
            ],
            row
        ]