# HEA Feature Engineering

"""
    This script creates an object called HEA which can be used to generate features for High Entropy Alloys.
    
    Method to generate features:
        Step 1: Import the class.
            code: from HEA_feature import HEA

        Step 2: Call the class. You need to pass a list of alloy names.
            code: hea = HEA(alloy_name)                                     alloy_name is list of alloy names. 
            
            Outcome: Three different excel files will be created in your working directory.
                alloy_composition.csv: This spreadsheet contains the composition of each element in each alloy for all the alloy.
                mixing_enthalpy.csv: This file contains two columns named 'Element 1' and 'Element 2'. They represent all the possible mixing
                                        pairs in the data.
                elemental_property.csv: This spreadsheet contains the list of elements as rows and elemental property as columns.
        
        Step 3: Add a third columns to the mixing_enthalpy.csv spreadsheet. This column should contain the mixing enthalpy for each pair.
                Fill all the reuired property in the elemental_property.csv spreadsheat. 
                !!!! DO NOT CHANGE THE FORMAT OF THESE SPREADSHEET !!!

        Step 4: Use the elemental_property method to pass in the updated spreadsheet as pandas Dataframe.
            Code: hea.elemental_property(data1,data2)       
                    where data1 is the pandas Dataframe createad from elemental_property.csv and 
                    data2 is the pandas Dataframe created from mixing_enthalpy.csv
        
        Step 5: Use the alloy_property method to obtain all the features.
            Code: hea.alloy_property.

    Features Calculated:
        1. Difference in Lattice Constants
        2. Difference in Melting Point
        3. Mixing Enthalpy
        4. Lattice Constants
        5. Lambda Parameter
        6. Difference in Atomic Radii
        7. Omega
        8. Melting Temp
        9. Difference in Electronegatiity
        10. Mixing Entropy
        11. Valence Electron Concentration
"""
# Importing required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from itertools import combinations

class HEA:
    
    # Initializer
    def __init__(self,name_list):
        self.name_list = name_list

    # Method to get alloy composition from alloy names
    def alloy_composition(self):
    
        ld = []                                                                 # list to store the composition of individual alloys
        
        for i in self.name_list:
            res_list = [s for s in re.split("([A-Z][^A-Z]*)", i) if s]          # this code splits the alloy name at each
                                                                                # capital letter 
                                                                                # eg: 'Al0.5CoCrCuFeNi' -> 
                                                                                # ['Al0.5','Co','Cr','Cu','Fe','Ni']
                        
            prop = dict() # a dictionary to store (element,composition) pairs for each alloy
            
            # this loops creates a dictionary where the keys are elements and values are the number preceding them
            # considering previous example:
            # ['Al0.5','Co','Cr','Cu','Fe','Ni'] -> {'Al':0.5, 'Co':0, 'Cr':0, 'Cu': 0, 'Fe': 0, 'Ni':0}
            for i in range(0,len(res_list)):
                comp = re.findall(r'[A-Za-z]+|\d+\.?\d*',res_list[i])           # this code splits the element name and no. preciding them
                                                                                # 'Al0.5' -> ['Al','0.5']
                if len(comp) == 2:
                    prop.update({comp[0]: float(comp[1])})
                else:
                    prop.update({comp[0] : 1})
            
            # this loop creates individual % composition for each elecment
            sum = 0
            for _,v in prop.items():
                sum += v

            for u,v in prop.items():
                prop.update({u:round((v/sum)*100,3)})
            
            ld.append(prop)                                                     # appends the dictionary to the list

        # Creating the composition table
        # An excel spreadsheet with the compositions will be saved in the directory
        # A copy of the dataset is assigned to self as self.composition
        final_dataframe = pd.DataFrame(ld)                                      # creating a dataframe using the list of dictionaries(creates some NA)
        final_dataframe = final_dataframe.fillna(0)                             # imputing NA's with zero
        list_df = [pd.DataFrame(self.name_list),final_dataframe]                # attaching the alloy names to the dataframe
        final = pd.concat(list_df, axis = 1) 
        final.to_csv('alloy_composition.csv', header = True, index = False)     # saving the dataframe to a csv file
        self.composition = final
        print("------------------------------------------------------------------------------------------------------------------")
        print(" ")
        print("Elemental Composition has been calculated. It can be found in alloy_composition.csv file in the directory.")
        print(" ")

        # The previously obtained list of dictionaries is assigned to self as self.alloy
        self.alloy = ld

        # The name of elements is assigned to self as self.elements
        self.elements = pd.DataFrame(final.iloc[:,1:final.shape[1]]).columns
        
        # The method to obtained mixing pairs is used to obtain the pairs
        # The pairs are saved to mixing_enthalpy.csv file
        pairs = self.mixing_pairs()
        pairs.to_csv('mixing_enthalpy.csv',header = True,index = False)
        print("New mixing_enthalpy.csv has been created. Add a new column with the mixing enthalpy of each pair.")

        # Creating the properties data set
        # A elemtal_properties.csv file will be created. This file should be populated with the required elemental properties.
        df1 = pd.DataFrame(columns = ['lattice_constants','electronegativity','melting_temp','atomic_radii','valence electron'])
        df2 = pd.DataFrame(self.elements, columns = ['Elements'])
        df3 = pd.concat([df2,df1])
        df3.to_csv("elemental_property.csv",header = True,index = False)
        print(" ")
        print("elemental_property.csv file has been created in the directory.")
        print("Fill the dataset with proper property")
        print(" ")
        print("------------------------------------------------------------------------------------------------------------------")
        # Guideline for next step
        print(" ")
        print("******************************************************************************************************************")
        print(" ")
        print("Use the elemental_prperty method to give the updated elemental_property.csv and mixing_enthalpy.csv file.")
        print("Make sure the supplied data is correct.")
        print(" ")
        print("******************************************************************************************************************")

    # Method to generate pairs of  Mixing
    def mixing_pairs(self):
        temp_pairs = []
        for i in range(0,len(self.composition)):                                # this loop generates all the mixing pairs of alloys
            hea = [s for s,_ in self.alloy[i].items()]
            temp_pairs.append(list(combinations(hea,2)))
        pairs = [item for sublist in temp_pairs for item in sublist]            # takes a list of list and creates a single list
        pairs = list({frozenset(c) for c in set(pairs)})                        # take only the distict pairs
        pairs = pd.DataFrame(pairs,columns=['Element 1','Element 2'])           # dataframe of above generated pairs
        pairs = pairs.sort_values(['Element 1','Element 2']).reset_index(drop = True)
        return pairs

    # Method to state the elemental property and mixing enthalpy
    def elemental_property(self,property,mix_enthalpy):
        if (set(property.iloc[:,0]) ==  set(self.elements)) & (property.shape[1] == 6) & (mix_enthalpy.shape[1] == 3):
            self.property = property
            self.mix_enthalpy = mix_enthalpy
            print(" ")
            print("******************************************************************************************************************")
            print(" ")
            print("Supplied Data has been accepted.")
            # Guideline for next step
            print(" ")
            print(" ")
            print("Use the alloy_property method to obtain all the features.")
            print(" ")
            print("******************************************************************************************************************")
        else:
            print("------------------------------------------------------------------------------------------------------------------")
            print(" ")
            print("Problems with supplied data. RECHECK.")
            print(" ")
            print("------------------------------------------------------------------------------------------------------------------")


    def lattice_constants(self):
        # getting the composition of elements from composition table
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]
        # getting the lattice constant for each element from property table
        elements_lattice = self.property.iloc[:,1]
        # calculating the mixing lattice constant by using matrix multiplication 
        lattice_const = np.matmul(np.array(elem_comp),np.array(elements_lattice))
        return pd.DataFrame(lattice_const/100)

    # Method for calculating difference in electronegativity
    def diff_electornegativity(self):
        # getting the composition of elements from the composition table
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]
        # getting the electronegativity of elements from the property table
        elements_elect = self.property.iloc[:,2]
        elems = []                                                              # a new list to store the difference in electronegativity
        # loop to iterate over all alloys
        for i in range(0,len(self.composition)):
            elem_names = [s for s,_ in self.alloy[i].items()]                                     # names of each element in alloy
            comp = [s for _,s in self.alloy[i].items()]                                           # % composition of each element in alloy
            elem_prop = list(self.property[self.property.iloc[:,0].isin(elem_names)].iloc[:,2])   # the electronegativity of each element in the alloy
            mean = (np.matmul(np.array(comp),np.array(elem_prop)))/sum(comp)                # weighted mean of the electronegativity for each alloy 
            temp_list = (elements_elect - mean)**2                                          # required calculation according to the formula
            diff_elect = np.matmul(np.array(elem_comp.iloc[i,:]/100),np.array(temp_list))   # matrix multiplication 
            elems.append(np.sqrt(diff_elect))
        return pd.DataFrame(elems)


    # Method for calculating mixing entropy
    def mix_entropy(self):
        entropy_mic = []                                                                 # list to store the results
        R = -8.31446261815324
        for i in range(0,len(self.composition)):
            temp = 0            
            for j in range(1,self.composition.shape[1]-1):
                # we do the calculation for only those elements that exist in the alloy so the value in composition table cannot be zero.
                if self.composition.iloc[i,j] != 0:
                    temp += (self.composition.iloc[i,j]/100)* np.log(self.composition.iloc[i,j]/100)                    # C_i * log(C_i)
            entropy_mic.append(R*temp)
        return pd.DataFrame(entropy_mic)


    # Method for calculating melting Temp by the rules of mixture.
    def melting_temp(self):                                                    
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]       # getting the composition of elements from the composition table
        elems_t = self.property.iloc[:,3]                                      # getting the melting temp from the property table
        t_m = np.matmul(np.array(elem_comp), np.array(elems_t))                # matrix multiplication
        return pd.DataFrame(t_m/100)
        
    # Method to calculate difference in atomic radii
    def atomic_radii(self):
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]       # getting the composition of elements from the composition table
        elems_radii = self.property.iloc[:,4]                                  # getting the atomic radii from the property table
        elems = []
        for i in range(0,len(self.composition)):
            elem_names = [s for s,_ in self.alloy[i].items()]                                     # names of each element in alloy
            comp = [s for _,s in self.alloy[i].items()]                                           # % composition of each element in alloy
            elem_prop = list(self.property[self.property.iloc[:,0].isin(elem_names)].iloc[:,4])   # the atomic radii of each element in the alloy
            mean = (np.matmul(np.array(comp),np.array(elem_prop)))/sum(comp)                      # weighted mean of the atomic radii for each alloy 
            temp_list = (1-(elems_radii/mean))**2                                                 # required calculation
            atm_rad = np.matmul(np.array(elem_comp.iloc[i,:]/100),np.array(temp_list))            # matrix multiplication
            elems.append(np.sqrt(atm_rad)*100)
        return pd.DataFrame(elems)

    # Method to calculate difference in lattice constants
    def diff_lattice_constants(self):
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]                         # getting the composition of elements from the composition table
        elements_lattice = self.property.iloc[:,1]                                               # getting the lattice constants from the property table
        elems = []
        for i in range(0,len(self.composition)):
            elem_names = [s for s,_ in self.alloy[i].items()]                                     # names of each element in alloy
            comp = [s for _,s in self.alloy[i].items()]                                           # % composition of each element in alloy
            elem_prop = list(self.property[self.property.iloc[:,0].isin(elem_names)].iloc[:,1])   # the lattice constants of each element in the alloy
            mean = (np.matmul(np.array(comp),np.array(elem_prop)))/sum(comp)                      # weighted mean of the lattice constants for each alloy 
            temp_list = (elements_lattice - mean)**2                                              # required calculation
            diff_lattice = np.matmul(np.array(elem_comp.iloc[i,:]/100),np.array(temp_list))       # matrix multiplication
            elems.append(np.sqrt(diff_lattice))                     
        return pd.DataFrame(elems)

    # Method to calculate diffenence in melting temperature
    def diff_melting_temp(self):
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]                         # getting the composition of elements from the composition table
        elements_melting = self.property.iloc[:,3]                                               # getting the lattice constants from the property table
        elems = []
        for i in range(0,len(self.composition)):
            elem_names = [s for s,_ in self.alloy[i].items()]                                     # names of each element in alloy
            comp = [s for _,s in self.alloy[i].items()]                                           # % composition of each element in alloy
            elem_prop = list(self.property[self.property.iloc[:,0].isin(elem_names)].iloc[:,3])   # the electronegativity of each element in the alloy
            mean = (np.matmul(np.array(comp),np.array(elem_prop)))/sum(comp)                      # weighted mean of the electronegativity for each alloy 
            temp_list = (elements_melting - mean)**2                                              # required calculation
            diff_melting = np.matmul(np.array(elem_comp.iloc[i,:]/100),np.array(temp_list))       # matrix multiplication
            elems.append(np.sqrt(diff_melting))
        return pd.DataFrame(elems)    

    # Method to generate the graphical parameter lambda
    def lambda_param(self):
        entropy_mix = self.mix_entropy()                                # using the mix_entropy method to calculate the mixing entropy
        diff_radii = self.atomic_radii()                                # using the atomic_radii method to calculate the difference in radii
        elems = []
        for i in range(0,len(self.composition)):
            temp = entropy_mix.iloc[i]/(diff_radii.iloc[i]**2)          # required calculations to obtain lambda
            elems.append(temp)
        return pd.DataFrame(elems)

    # Method to generate Valence Electron Concentration
    def valence_electron(self):
        elem_comp = self.composition.iloc[:,1:self.composition.shape[1]]    # getting the composition of each elements
        v_electron = self.property.iloc[:,5]                                # getting the valence electron property
        temp = np.matmul(np.array(elem_comp),np.array(v_electron))          # required calculations
        return pd.DataFrame(temp/100)

    # Method to generate Enthalpy of Mixing
    def enthalpy_mixing(self):
        enthalpy = []
        for i in range(0,len(self.composition)):
            hea = [s for s,_ in self.alloy[i].items()]                      # obtaining all the elements
            temp_pairs = list(combinations(hea,2))                          # creates the pairs for mixing using the elements
            current_dict = self.alloy[i]                                    
            calc = 0
            for mix in temp_pairs:                                          # this loop iterates over each pair
                # obtaining the mixing enthalpy for the pair
                # searches for the first element of pair in the 'Element 1' column and second element of pair in 'Element 2' column
                # if the search doesn't find the pair the size of temp_enthalpy is 0
                
                temp_enthalpy = self.mix_enthalpy.loc[(self.mix_enthalpy['Element 1'] == mix[0]) & (self.mix_enthalpy['Element 2'] == mix[1])].iloc[:,2]
                
                # the if statement below states that if size of temp_entalpy is zero then reverse the order of search
                # i.e. 
                # searches for the second element of pair in the 'Element 1' column and first element of pair in 'Element 2' column

                if temp_enthalpy.size == 0 :
                    temp_enthalpy = self.mix_enthalpy.loc[(self.mix_enthalpy['Element 1'] == mix[1]) & (self.mix_enthalpy['Element 2'] == mix[0])].iloc[:,2]
                temp_enthalpy = temp_enthalpy.iloc[0]

                # required calculations
                calc += 4*temp_enthalpy*current_dict[mix[0]]*current_dict[mix[1]]/10000     

            enthalpy.append(calc)    
        return pd.DataFrame(enthalpy)

    # Method to generate omega
    def omega(self):
        Tm = self.melting_temp()                        # using melting_temp method to obtain the melting temperature
        enthalpy = self.enthalpy_mixing()               # using enthalpy_mixing method to obtain the mixing enthalpy
        entropy = self.mix_entropy()                    # using mix_entropy method to obtain the mixing entropy
        prop = []
        for i in range(0,len(self.composition)):        # iterating over each alloy
            temp = Tm.iloc[i]*entropy.iloc[i]/np.abs(enthalpy.iloc[i])      # required calculation for each alloy
            prop.append(temp)
        return pd.DataFrame(prop)

    # Method to generate all properties at once
    def alloy_property(self):
        #getting the alloy names
        alloy_name = pd.DataFrame(self.name_list)
        print(" ")
        print("******************************************************************************************************************")
        print(" ")
        print("Generating Features.")
        print(" ")


        # generating all the features using above defined functions 
        prop1 = self.diff_lattice_constants()
        print("Difference in Lattice Constants Generated.")
        prop2 = self.diff_melting_temp()
        print("Difference in Melting Point Generated.")
        prop3 = self.enthalpy_mixing()
        print("Mixing Enthalpy Generated.")
        prop4 = self.lattice_constants()
        print("Lattice Constants Generated.")
        prop5 = self.lambda_param()
        print("Lambda Parameter Generated.")
        prop6 = self.atomic_radii()
        print("Difference in Atomic Radii Generated.")
        prop7 = self.omega()
        print("Omega Generated")
        prop8 = self.melting_temp()
        print("Melting Temp Generated.")
        prop9 = self.diff_electornegativity()
        print("Difference in Electronegatiity Generated.")
        prop10 = self.mix_entropy()
        print("Mixing Entropy Generated.")
        prop11 = self.valence_electron()
        print("Valence Electron Concentration Generated.")
        print(" ")

        # Creating the Features Dataset
        Features = pd.concat([alloy_name,prop1,prop2,prop3,prop4,prop5,prop6,prop7,prop8,prop9,prop10,prop11],axis = 1)
        Features.columns = ["Alloy","Diff. Lattice Constants","Diff. Melting Point","Mixing Enthalpy","Lattice Constants","Lambda","Diff. in atomic radii",
                            "Omega","Melting Temp.","Diff. Electronegativity","Mixing Entropy","Valence electron"]
        
        # Saving the Feature Dataset as a .csv file
        Features.to_csv("Alloy_Features.csv",header = True)
        print(" ")
        print("Features Generated in Directory.")
        print(" ")
        print("******************************************************************************************************************")
