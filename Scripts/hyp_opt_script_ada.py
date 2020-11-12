from Youngs_Modulus import Youngs_Modulus
import pandas as pd 
import sys

sys.stdout = open('output_ada.txt','w')

data = pd.read_csv("training_new.csv")

youngs = Youngs_Modulus(data)
youngs.preprocessing()

grid_values = {
    'n_estimators': [100,150,200,250,300,350,400,450,500],
    'learning_rate': [0.001, 0.003, 0.007, 0.009, 0.01, 0.03],
}

best_params, best_scores = youngs.optimizer_ada(grid_values)

youngs.feature_importance()

validation = pd.read_csv("validation_new.csv")
results = youngs.test(validation)
print(results)

sys.stdout.close()
