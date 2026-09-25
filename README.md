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
______________________________________________
<h2>By MACsepehri</h2>
<a href='mailto:macsepehri@gmail.com'>Contact with E-mail</a>