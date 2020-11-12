from Youngs_Modulus import Youngs_Modulus
import pandas as pd 
import sys

sys.stdout = open('output_ada_refractory.txt','w')

data = pd.read_csv("Youngs_Data_Refractory.csv")

youngs = Youngs_Modulus(data)
youngs.preprocessing()

grid_values = {
    'n_estimators': [100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000],
    'learning_rate': [0.01, 0.03, 0.05, 0.07, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.3, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.5],
}

best_params, best_scores = youngs.optimizer_ada(grid_values)

youngs.feature_importance()

validation = pd.read_csv("validation_data.csv")
results = youngs.test(validation)
print(results)

sys.stdout.close()
