import pandas as pd
from HEA_feature import HEA

#Loading the data
data = pd.read_csv("alloy_name.csv")

# Extracting the alloy names
alloy_name = data.iloc[:,0]

# calling the HEA object
hea = HEA(alloy_name)

# using the alloy_composition method
hea.alloy_composition()

#Loading the property dataset
prop = pd.read_csv("elemental_property_updated.csv")
pairs = pd.read_csv("mixing_enthalpy_updated.csv")

# using the elemental_property method
hea.elemental_property(prop,pairs)

# Generating the alloy features using the alloy_proprty method
hea.alloy_property()
