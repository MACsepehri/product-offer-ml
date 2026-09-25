from ml_model import ml_model

model = ml_model()
model.fit_data()
user = model.rand_user

predict_result = model.predict(user)
# ------------------------------------------
print(f'Proposal Offer: {predict_result["offer"]}')
print(f'Proposal Product Data: \n')
for data in predict_result['product']:
    print(data, "  :  ", predict_result['product'][data])