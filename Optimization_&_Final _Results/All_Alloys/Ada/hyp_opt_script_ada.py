from Youngs_Modulus import Youngs_Modulus
import pandas as pd 
import sys

sys.stdout = open('output_ada.txt','w')

data = pd.read_csv("Youngs_Data_All.csv")

youngs = Youngs_Modulus(data)
youngs.preprocessing()

grid_values = {
    'n_estimators': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
    'learning_rate': [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.18, 0.20, 0.23, 0.26, 0.29, 0.3, 0.33, 0.36, 0.39, 0.4, 0.43, 0.46, 0.49, 0.5],
}

best_params, best_scores = youngs.optimizer_ada(grid_values)

youngs.feature_importance()

validation = pd.read_csv("validation_data.csv")
results = youngs.test(validation)
print(results)

sys.stdout.close()
