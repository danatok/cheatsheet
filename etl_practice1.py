# Reading data from json, taking only chili receipts and based on the preparation and cooking time, trying to find overall level of cooking complexity

import pandas as pd
import numpy as np

# Reading the json files, make sure that json file is in the same directory where your script is.
df = pd.read_json('recipes.json', lines = True)

# Check for all the versions of the word 'Chilies', considering mispelled ones and singular version. 
df_chili = df[df['ingredients'].str.contains('Chilies') | df['ingredients'].str.contains('Chiles') | df['ingredients'].str.contains('Chili') | df['ingredients'].str.contains('Chilis') ]

#Resetting index for convenience 
df_chili = df_chili.reset_index(drop = True)

# As the fields in the prepTime and cookTime contain time in the format of 'PT...m' which is not convenient to work with, 
# only the integers were extracted.
df_chili['prepTime'] =df_chili['prepTime'].str.extract('(\d+)')
df_chili['cookTime'] =df_chili['cookTime'].str.extract('(\d+)')

# To get rid of Nan values, they were converted to a large negative number. However more robust solution is needed in future. 
# Further they were converted to int values.
df_chili['prepTime'] = df_chili['prepTime'].fillna(-100)
df_chili['prepTime'] = df_chili['prepTime'].astype(int)

df_chili['cookTime'] =df_chili['cookTime'].fillna(-100)
df_chili['cookTime'] =df_chili['cookTime'].astype(int)

# In order to create a new column, we need to calculate the total cooking time. The following code creates consitions for Easy, Medium and Hard cases.
# As I converted the Nan values to large negative numbers, I assume that their sum will result in a negative number.
conditions = [
    (df_chili['prepTime'] + df_chili['cookTime'] > 60),
    ((df_chili['prepTime'] + df_chili['cookTime'] >= 30) & (df_chili['prepTime'] + df_chili['cookTime'] <= 60 ) ),
    ( (df_chili['prepTime'] + df_chili['cookTime'] < 30) & (df_chili['prepTime'] + df_chili['cookTime'] > 0 ) ),
    (df_chili['prepTime'] + df_chili['cookTime'] < 0)
    ]

# create a list of the values we want to assign for each condition
values = ['Hard', 'Medium', 'Easy', 'Unknown']

# create a new column and use np.select to assign values to it using our lists as arguments
df_chili['difficulty'] = np.select(conditions, values)

# Saving to csv file
df_chili.to_csv('chili_recipes.csv', index = False)
