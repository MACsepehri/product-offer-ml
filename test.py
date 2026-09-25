from ml_model import ml_model

model = ml_model()
model.fit_data()
user = model.rand_user

predict_result = model.predict(user)
print(predict_result)