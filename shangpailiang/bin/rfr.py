import numpy as np
import pandas
import pickle
import xgboost
from sklearn.cross_validation import train_test_split
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import time
from data import load_data

print("Load and process datasets.")
(X_train, Y_train, X_valid, Y_valid, X_test, train, test) = load_data()

print("Training model. This may take awhile...")
rfr = RandomForestRegressor(criterion='mse')
# rfr = RandomForestRegressor(n_estimators=300,
#                            criterion='mse', max_depth=25, min_samples_split=5, min_samples_leaf=1,
#                            min_weight_fraction_leaf=0.0, max_features='auto')
rfr.fit(X_train, Y_train)
print(rfr.feature_importances_)
print("Validating the model.")
score = rfr.score(X_valid, Y_valid)
print("Score-rfr: ", score)
yhat = rfr.predict(X_valid)
print('MSE-rfr: ', mean_squared_error(Y_valid, yhat))

print("Making predictions on the test set.")
predictions = rfr.predict(X_test)

print("Saving predictions to csv file for submission.")
result = pandas.DataFrame(
    {"date": test["date"], "brand": test["brandid"], "cnt": predictions})
result = result[['date', 'brand', 'cnt']]
result['cnt'] = result['cnt'].astype(int)
result['date'] = result['date'].astype(int)
result['brand'] = result['brand'].astype(int)
result.to_csv('../output/rfr.csv', index=False)

print("Done")
