# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 13:28:13 2018

@author: Andy
"""
#Makes table with damage summary by champion
#import numpy as np
import pandas as pd


def RecapTabler(header, fightid, df4):
    
    #champorinos = list(df4.Champion.unique())
    
    #Cumulative damages from each champ
    tot_dmg = df4.groupby(['Champion', 'Type']).agg({'Total':'sum'})
    tot_dmg = tot_dmg.unstack(1)
    tot_dmg = tot_dmg.fillna(0)
    #Total Damage per champion
    total_dmg = df4.groupby(['Champion']).agg({'Total':'sum'})
    total_dmg = total_dmg.fillna(0)
    damages = pd.concat([tot_dmg, total_dmg], axis = 1)
    #Max damage from one ability from each champion
    max_dmg = df4.groupby(['Champion']).agg({'Total':'max'})
    sample = df4[["Ability", "Total", "Champion"]]
    max_dmg = max_dmg.merge(sample)
    #Deleting duplicate row if two highest dmg abilities for one champion, changing index
    max_dmg = max_dmg.drop_duplicates(subset = ["Champion"])
    max_dmg = max_dmg.drop(["Champion"], 1)
    max_dmg.index = damages.index
    #Putting everything together
    table = pd.concat([damages, max_dmg], axis = 1) 
    #Dropping useless column
    table = table.drop(("Total","None"), 1)
    #Formatting headers
    if sum(df4["Type"] == "True") != 0:
        table.columns = ["Total Magical Damage", "Total Physical Damage", "Total True Damage", "Total Damage", "Most Damage in One Ability", "Highest Damage Ability"]
    else:
        table.columns = ["Total Magical Damage", "Total Physical Damage", "Total Damage", "Most Damage in One Ability", "Highest Damage Ability"]
    table["FightID"] = fightid
    cols = table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    table = table[cols]
    table["Highest Damage Ability"] = table["Highest Damage Ability"] + " - " + table["Most Damage in One Ability"].astype(str)
    table = table.drop(["Most Damage in One Ability"], 1)    
    return table