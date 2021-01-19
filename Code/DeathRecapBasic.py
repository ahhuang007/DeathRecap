
# Andy Huang
# 3/27/18
# Death Recap Project, Basic Plots


import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc, output_file, show
from bokeh.models.widgets import Panel, Tabs


#Preliminary stuff
wk_dir = "C:\\Users\\Andy\\Documents\\DeathRecapProject\\Data\\"
data = pd.read_excel(wk_dir+"test6.xlsx")

#Number of fights transcribed
fights = list(data.FightID.unique())



#Melting data because Alex wants me to
data["Index"] = pd.Series(range(len(data)))
common_vars = ['FightID','Time','Champion','Ability','Duration','CC','CCDuration','Index', 'Image', 'CCImage']

data1=data[common_vars+['Total','Type']]

data2=data[common_vars+['Total2','Type2']]

data2=data2[~data2.Total2.isnull()] # keep only rows that had damage

data2=data2.rename(columns={'Total2':'Total','Type2':'Type'}) # rename colnames so they match

new_data = data1.append(data2).sort_values('Index')



#Cumulative damage over time
#Separating between fights

#Variable prev is needed since the index in dataframe df used in the function starts from wherever it was in data
prev = 0
prev2 = 0
#Making blank columns to add values in
new_data["cumulative_dmg"] = np.zeros(len(new_data))
new_data["cumulative_magic"] = np.zeros(len(new_data))
new_data["cumulative_phys"] = np.zeros(len(new_data))
new_data["cumulative_true"] = np.zeros(len(new_data))
#Resetting index
new_data = new_data.reset_index(drop = True)
#Looping cumulative damage for each fight
for count in range(len(fights)):
    #Isolating the dataa from one fight
    df = new_data[new_data.FightID == count + 1]
    
    #Call DamageSum function, add results to data
    new_data["cumulative_dmg"][prev:prev + len(df)] = DamageSum(df, prev, df["Type"] != None)
    new_data["cumulative_magic"][prev:prev + len(df)] = DamageSum(df, prev, df["Type"] == "Magical")
    new_data["cumulative_phys"][prev:prev + len(df)] = DamageSum(df, prev, df["Type"] == "Physical")
    new_data["cumulative_true"][prev:prev + len(df)] = DamageSum(df, prev, df["Type"] == "True")
    #Update prev value
    prev = prev + len(df)

#List of all champions in all fights
bigchampions = list(new_data.Champion.unique())
#Creating columns for cumulative damage from each champion
for count5 in range(len(bigchampions)):
    new_data["cumulative_" + bigchampions[count5]] = np.zeros(len(new_data))
#Looping for damage from each champion in each fight
for count3 in range(len(fights)):
    #Isolating data from one fight
    df3 = new_data[new_data.FightID == count3 + 1]
    #List of relevant champions, excludes null columns
    champions = list(df3.Champion.unique())
    #Loop to add damages to the right column and rows
    for count4 in range(len(champions)):
        
        new_data["cumulative_" + champions[count4]][prev2:prev2 + len(df3)] = DamageSum(df3, prev, df3["Champion"] == champions[count4])
    #Updating prev2 value    
    prev2 = prev2 + len(df3)

#Gathering data for summary table
names = ["Total Magic Damage", "Total Physical Damage", "Total True Damage", "Total Damage", "Most Damaging Ability"]
datatables = []
prev5 = 0

for count10 in range(len(fights)):
    df5 = new_data[new_data.FightID == count10 + 1]
    datatables.append(RecapTabler(names, count10 + 1, df5))
    prev5 = prev5 + 5

#Creating subplots

for count9 in range(len(fights)):
    
#Looping plotter function for each fight
    
    df2 = new_data[new_data.FightID == count9 + 1]
    RecapPlotter(df2, count9 + 1)
    #BarPlot(df2, count9 + 1)









