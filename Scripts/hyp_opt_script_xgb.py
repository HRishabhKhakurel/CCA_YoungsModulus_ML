from Youngs_Modulus import Youngs_Modulus
import pandas as pd 
import sys

sys.stdout = open('output_xgb.txt','w')

data = pd.read_csv("Final_Youngs_Data.csv")

youngs = Youngs_Modulus(data)
youngs.preprocessing()

grid_values = {
    'n_estimators': [100,200,300,400,500,600,700,800,900,1000],
    'learning_rate': [0.01, 0.03, 0.05, 0.07, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.3, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.5],
    'max_features': ['sqrt','log2','auto'],
    'max_depth': [3,4,5,6,8],
    'criterion': ['mse','mae','friedman_mse'],
    'min_samples_leaf': [1,2,3],
    'min_samples_split': [2,3,4]
}

best_params, best_scores = youngs.optimizer_xgb(grid_values)

youngs.feature_importance()

validation = pd.read_csv("Validation_set_features.csv")
results = youngs.test(validation)
print(results)

sys.stdout.close()
