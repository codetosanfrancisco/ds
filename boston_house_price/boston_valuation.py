from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd

# Gather Data
boston_dataset = load_boston()
data = pd.DataFrame(data=boston_dataset.data, columns=boston_dataset.feature_names)

features = data.drop(['INDUS','AGE'],axis=1)

log_prices = np.log(boston_dataset.target)
target = pd.DataFrame(data=log_prices, columns=['PRICE'])

property_stats = features.mean().values.reshape(1,11)

regr = LinearRegression().fit(features, target)
fitted_vals = regr.predict(features)


# Challenge
MSE = mean_squared_error(target, fitted_vals)
RMSE = np.sqrt(MSE)

RM_IDX = 4
PTRATIO_IDX = 8
CHAS_IDX = 2
ZILLOW_MEDIAN_PRICE = 583.3
SCALE_FACTOR = ZILLOW_MEDIAN_PRICE/ np.median(boston_dataset.target)

def get_log_estimate(nr_rooms, students_per_classroom, next_to_river=False, high_confidence=True):
    
    # Configure property
    property_stats[0][RM_IDX] = nr_rooms
    property_stats[0][PTRATIO_IDX] = students_per_classroom
    
    if next_to_river:
        property_stats[0][CHAS_IDX] = 1
    else:
        property_stats[0][CHAS_IDX] = 0
        
    
    # Make Predictions
    log_estimate = regr.predict(property_stats)[0][0]
    
    # Calc range
    if high_confidence:
        upper_bound = log_estimate + 2*MSE
        lower_bound = log_estimate - 2*MSE
        interval = 95
    else:
        upper_bound = log_estimate + MSE
        lower_bound = log_estimate - MSE
        interval = 68
        
    return log_estimate, upper_bound, lower_bound, interval

def get_dollar_estimate(rm, ptratio, chas=False, large_range=True):
    
    # Docstring for documentation (Shift tab to see)
    """
    Estimate price of a property in Boston.
    Keyword arguments:
    rm -- number of rooms in the property
    ptratio -- number of students per teacher in the classroom for the school in the area
    chas -- True if the property is next to the river, False otherwise
    large_range -- True for a 95% prediction interval, False for a 68% interval 
    """
    
    if rm < 1 or ptratio < 1:
        print("This is unrealistic. Try again!")
        return
    
    log_est, upper, lower, conf = get_log_estimate(rm, students_per_classroom=ptratio,
                            next_to_river=chas, high_confidence=large_range)


    # Calculate today's dollar
    dollar_est = np.e**log_est * 1000 * SCALE_FACTOR
    dollar_hi = np.e**upper * 1000 * SCALE_FACTOR
    dollar_low = np.e**lower * 1000 * SCALE_FACTOR

    # ROund the dollar values to nearest thousand
    rounded_est = np.around(dollar_est, -3)
    rounded_hi = np.around(dollar_hi, -3)
    rounded_low = np.around(dollar_low, -3)

    print(f'The estimated property value is {rounded_est}')
    print(f'At {conf}% confidence the valuation range is')
    print(f'USD {rounded_low} at the lower end to USD {rounded_hi} at the high end.')

