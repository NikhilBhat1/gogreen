import pandas as pd
import numpy as np
dataset = pd.read_csv('nutrition.csv')

            

dataset['carbohydrates_100g'].isin(range(20))
low_carb=dataset.loc[dataset['carbohydrates_100g']==True]
#carb=low_carb['product_name']
print(low_carb.product_name)

dataset['energy_100g'].isin(range(1500,3000))
energy_booster=dataset.loc[dataset['energy_100g']==True]
#energy=energy_booster['product_name']
print(energy_booster.product_name)


#print(np.array(energy))
