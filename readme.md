# Machine Learning Assisted Young's Modulus Prediction of Compositionally Complex Alloys 

This repository consists of scripts, notebooks and datasets used for the above titled project that has been performed during Summer 2020 at Pacific Northwest National Laboratory(PNNL) sponsored by the NSF-Mathematical Sciences Summer Graduate Internship.

## Goal of the project: 
Compositionally Complex Alloys(CCAs) are alloys made up of more than 2 metallic elements. Our goal was to use Machine Learning Techniques to predict the Young's Modulus of these metals.
	
## Method 
The first step of our project was to automate the feature engineering process for these CCAs. This consisted of breaking down the name of alloys using string processing into individual elements and their composition in the alloys. Then collecting the data for these individual alloys(which are readily available from past research). Finally using method of mixtures to calculate the properties for these alloys.
Once the features have been generated, we trained the Machine Learning models. We selected three different algorithms - "Gradient Boosting", "Ada Boost" and "XGBoost". Cross-\Validation was done to get robust training and testing errors and the best model among these was identified. Finally we made final predictions on the testing data set. We also looked at the feature importances for each of the models.
We are in the process of publishing our results.
			
This repository consists of 4 sub folders which comprises of the following:

1. Feature Generation
This folder consists of the script to generate features for CCAs. Inside this folder are three subfolders. One for the dataset with all alloys, one with only refractory alloys and one with the validation or testing dataset. The script **HEA_feature.py** is the major script which has been written following object oriented guidelines for generating the features. This script has been called in the **feature_generation.py** in each of the subfolders.

2.  Scripts
This folder consists of all the major scripts used in our project. Here  is the a brief description of all the scripts inside:\
	* _HEA\_feature.py_: An object oriented script that defines objects and methods to	generate features for CCAs\
	* _feature\_generation.py_ : This script is the implementation of the **HEA_feature.py** script.\
	*_Youngs\_Modulus.py_: This script is the major script that creates an object with methods f or each ML model, feature importance extraction, and result visualization.\
	* _hyp\_opt\_script\_ada.py_: The implementation of **Youngs_Modulus.py** for Ada Boost ML model.\
	* _hyp\_opt\_script\_gbr.py_: The implementation of **Youngs_Modulus.py** for Gradient Boosting Model.\
	* _hyp\_opt\_xgb.py_: The implementation of **Youngs_Modulus.py** for XGBoost Model.
	
3. Optimization\_&\_Final_Results: 
	This folder consists of scripts to perform final hyperparameter optiomization, correlation analysis and feature importance extraction  for both the dataset with only refractory alloys and dataset with all alloys.
	
4. Ad-hoc analysis_notebooks:
	This folder consists of jupyter notebooks where we performed preliminary analysis on the data and did an ad-hoc implementation of the model before finalyizing our models and methods.
	
	

