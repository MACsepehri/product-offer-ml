# product-offer-ml
product-offer-ml is a small model for online shops to give their product info and user info with some
sample data for prediction. then the app start predicting to check is it good to give a offer for the
given user or not, if it was, it will going to find the most similar product by the user cart and products
that user bought.
The product dataset columns must be like this :
<p>product_id,product_name,category,subcategory,brand,price,original_price,discount_percent,stock,rating,review_count,sales_count,view_count,cart_add_count,wishlist_count,return_rate,seller_count,shipping_days,is_original,color,weight_grams,demand_score,popularity_score,target_sales_next_7_days</p>
And the users dataset columns :
<p>username,category,price,original_price,total_products_discount_percent,stock,in_cart,bought_it</p>

for filling your datasets, you can see our sample datasets :<br>
<a href='./all.csv'>Products Dataset</a><br>
<a href='./user.csv'>Users Dataset</a>
------------------------------------------------
a small usage :
<pre>
from ml_model import ml_model

model = ml_model()
model.fit_data(product_data_filepath='your_product_csv_data.csv', user_data_filepath='your_user_csv_data.csv') # will fit the user informations
user = model.rand_user # it returns a list, for more info check the function.

predict_result = model.predict(user) # returns a dict of the most similar product and a offer.
print(predict_result)
</pre>
----------------------------------------------------
Another usage + Result: 
<pre>
from ml_model import ml_model

model = ml_model()
model.fit_data()
user = model.rand_user

predict_result = model.predict(user)

print(f'Proposal Offer: {predict_result.offer}')
print(f'Proposal Product Data: \n')
for data in predict_result.product:
    print(data, "  :  ", predict_result.product[data])
</pre>
<p>Result of a random user :</p>
<pre>
Proposal Offer: 21%
Proposal Product Data: 
# ---- products that user might buy them ---- #
product_id   :   10045
product_name   :   Cougar Advanced
category   :   Gaming
subcategory   :   Gaming Chair
brand   :   Cougar
price   :   15552810
original_price   :   19201000
discount_percent   :   19
stock   :   618
rating   :   5
review_count   :   7532
sales_count   :   6339
view_count   :   989258
cart_add_count   :   64637
wishlist_count   :   12610
return_rate   :   0.034
seller_count   :   14
shipping_days   :   1
is_original   :   1
color   :   Black
weight_grams   :   2543
demand_score   :   79.6
popularity_score   :   75.1
target_sales_next_7_days   :   237
</pre>
______________________________________________
<h2>By MACsepehri</h2>
<a href='mailto:macsepehri@gmail.com'>Contact with E-mail</a>
