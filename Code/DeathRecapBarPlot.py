# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 01:37:06 2018

@author: Andy
"""

import numpy as np
import pandas as pd

from bokeh.models import HoverTool, Label
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.io import output_file, show, curdoc

def BarPlot(df, fightid):
    
    champoninos = list(df.Champion.unique())
    types = ["Magical Damage", "Physical Damage", "True Damage"]
    colors = ["#315DFF", "#FFD00B", "#E5E5E5"]
    
              
    '''hoverm = HoverTool(tooltips="""
    <div>
        <div>
            <img
                src="@img" height="42" alt="@img" width="42"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 17px; font-weight: bold;">@desc</span>
        </div>
        <div>
            <span style="font-size: 15px;">@dmg</span>
        </div>
    </div>
    """
    )'''
              
    bplot = figure(x_range = champoninos, plot_height = 250, title = "stuff")
    
    totals = pd.DataFrame()
    totals = df.groupby(['Champion', 'Type']).agg({'Total':'sum'})
    totals = totals.unstack(1)
    totals = totals.fillna(0)
    totals = totals.drop(("Total", "None"), 1)
    totals.columns = ["Magical Damage", "Physical Damage", "True Damage"]
    totals = totals.reset_index()
    
    data = {'champs' : champoninos,
            'Magical Damage' : totals["Magical Damage"],
            'Physical Damage' : totals["Physical Damage"],
            'True Damage' : totals["True Damage"]
            }
    
    test1 = {'champs' : ["Kassadin", "Lulu", "Renekton", "Vayne"],
             'Magical Damage' : [258, 0, 240, 0],
             'Physical Damage' : [0, 0, 496, 851],
             'True Damage' : [0, 0, 0, 230]}
    
    bplot.vbar_stack(types, x = "champs", width = 0.9, color = colors, source = test1, legend = [value(x) for x in types])
    
    bplot.y_range.start = 0
    bplot.x_range.range_padding = 0.1
    bplot.xgrid.grid_line_color = None
    bplot.axis.minor_tick_line_color = None
    bplot.outline_line_color = None
    bplot.legend.location = "top_left"
    bplot.legend.orientation = "horizontal"
    
    
    output_file("bar.html")
    show(bplot)
    