# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 06:39:31 2018

@author: Andy
"""
import numpy as np

import pandas as pd

from bokeh.models import HoverTool, Label
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Div, DatetimeTickFormatter
from bokeh.io import output_file, show, curdoc
from bokeh.models.widgets import Panel, Tabs
from bokeh.models.glyphs import ImageURL
from bokeh.core.properties import value

def RecapPlotter(df, fightid):
    #Return two plots: One with cumulative damage and magic damage lines plotted, shaded to show phys/mag
    #Other plot will show damage from each champion
    totalhp = sum(df.Total)
    hpmag = max(df.cumulative_magic)
    df = df.reset_index(drop = True)
    df["HP_remaining"] = totalhp - df.cumulative_dmg
    df["HP_mag"] = hpmag - df.cumulative_magic
    df.Time = df.Time * 1000
    df.CCDuration = df.CCDuration * 1000
    #First plot
    #Time data
    ex = df.Time
    
    #Cumulative damage data
    wai = df.HP_remaining
    
    #Cumulative magic damage data
    wai2 = df.HP_mag

    #Plotting lines
    right = (max(df.Time) - min(df.Time)) / 50
    #May god have mercy on the soul I have left
    temp = pd.DataFrame()
    temp["Time"] = np.zeros(len(df) + len(df) - 1)
    temp["CoordP"] = np.zeros(len(df) + len(df) - 1)
    temp["CoordM"] = np.zeros(len(df) + len(df) - 1)
    temp.loc[0, "Time"] = min(ex)
    temp.loc[0, "CoordP"] = totalhp
    temp.loc[0, "CoordM"] = hpmag
    for counter in range(len(df) - 1):
        temp.loc[(2 * counter) + 1, "Time"] = ex[counter]
        temp.loc[(2 * counter) + 1, "CoordP"] = wai[counter]
        temp.loc[(2 * counter) + 1, "CoordM"] = wai2[counter]
        temp.loc[(2 * counter) + 2, "Time"] = ex[counter + 1]
        temp.loc[(2 * counter) + 2, "CoordP"] = wai[counter]
        temp.loc[(2 * counter) + 2, "CoordM"] = wai2[counter]
    dfm = df[df["Type"] == "Magical"]
    dfm  = dfm.reset_index(drop = True)
    dfm["Right"] = dfm["Time"] + right
    dfm["Bottom"] = np.zeros(len(dfm))
    for count14 in range(len(dfm) - 1):
        dfm["Bottom"] = dfm["cumulative_magic"] - dfm["Total"]
    dfp = df[df["Type"] == "Physical"]
    dfp = dfp.reset_index(drop = True)
    dfp["Right"] = dfp["Time"] + right
    dfp["Bottom"] = np.zeros(len(dfp))
    dfp["Bottom"] = dfp["cumulative_phys"] - dfp["Total"]
    dftt = df[df["Type"] == "True"]
    dftt  = dftt.reset_index(drop = True)
    dftt["Right"] = dftt["Time"] + right
    dftt["Bottom"] = np.zeros(len(dftt))
    dftt["Bottom"] = dftt["cumulative_true"] - dftt["Total"]
    dft = df
    dft["Right"] = dft["Time"] + right
    dft["Bottom"] = np.zeros(len(dft))
    dft["Bottom"] = dft["HP_remaining"]
    dftrue = dft[dft["Type"] == "True"]
    dftrue = dftrue.reset_index(drop = True)
    dftmag = dft[dft["Type"] == "Magical"]
    dftmag = dftmag.reset_index(drop = True)
    dftphys = dft[dft["Type"] == "Physical"]
    dftphys = dftphys.reset_index(drop = True)
    source = ColumnDataSource(df)
    source2 = ColumnDataSource(temp)
    
    
    
    sourcehoverm = ColumnDataSource(data = dict(top = dfm.cumulative_magic, 
                                                left = dfm.Time, 
                                                bottom = dfm.Bottom, 
                                                right = dfm.Right, 
                                                desc = dfm.Champion + " - " + dfm.Ability, 
                                                img = dfm.Image,
                                                dmg = dfm.Total.astype(str) + " Damage"
                                                ))
    sourcehovertphys = ColumnDataSource(data = dict(top = dftphys.HP_remaining + dftphys.Total, 
                                                left = dftphys.Time, 
                                                bottom = dftphys.Bottom, 
                                                right = dftphys.Right, 
                                                desc = dftphys.Champion + " - " + dftphys.Ability, 
                                                img = dftphys.Image,
                                                dmg = dftphys.Total.astype(str) + " Damage"
                                                ))
    sourcehovertrue = ColumnDataSource(data = dict(top = dftrue.HP_remaining + dftrue.Total, 
                                                left = dftrue.Time, 
                                                bottom = dftrue.Bottom, 
                                                right = dftrue.Right, 
                                                desc = dftrue.Champion + " - " + dftrue.Ability, 
                                                img = dftrue.Image,
                                                dmg = dftrue.Total.astype(str) + " Damage"
                                                ))
    sourcehovertmag = ColumnDataSource(data = dict(top = dftmag.HP_remaining + dftmag.Total, 
                                                left = dftmag.Time, 
                                                bottom = dftmag.Bottom, 
                                                right = dftmag.Right, 
                                                desc = dftmag.Champion + " - " + dftmag.Ability, 
                                                img = dftmag.Image,
                                                dmg = dftmag.Total.astype(str) + " Damage"
                                                ))
    sourcehoverp = ColumnDataSource(data = dict(top = dfp.cumulative_phys, 
                                                left = dfp.Time, 
                                                bottom = dfp.Bottom, 
                                                right = dfp.Right, 
                                                desc = dfp.Champion + " - " + dfp.Ability, 
                                                img = dfp.Image,
                                                dmg = dfp.Total.astype(str) + " Damage"
                                                ))
    sourcehovertt = ColumnDataSource(data = dict(top = dftt.cumulative_true, 
                                                left = dftt.Time, 
                                                bottom = dftt.Bottom, 
                                                right = dftt.Right, 
                                                desc = dftt.Champion + " - " + dftt.Ability, 
                                                img = dftt.Image,
                                                dmg = dftt.Total.astype(str) + " Damage"
                                                ))
    
    hoverm = HoverTool(tooltips="""
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
    )
   
    plot = figure(x_axis_label = "Time", y_axis_label = "Health Remaining", tools = [], plot_width = 700, plot_height = 600)
    val = min(df.Time) + 0.75 * ((max(df.Time) - min(df.Time)) / 2)
    text = Label(x = val, y = 100, text = " Crowd Control ", border_line_color = "black")
    plot.add_layout(text)
    plot.title.text_font = "times"
    plot.xaxis.axis_label_text_font = "arial"
    plot.xaxis.axis_label_text_font_size = "16pt"
    plot.xaxis.axis_label_text_font_style = "bold"
    plot.yaxis.axis_label_text_font = "arial"
    plot.yaxis.axis_label_text_font_size = "16pt"
    plot.yaxis.axis_label_text_font_style = "bold"
    plot.yaxis.major_label_orientation = "horizontal"
    plot.xaxis.major_label_text_font_size = "10pt"
    plot.yaxis.major_label_text_font_size = "10pt"
    plot.xaxis[0].formatter = DatetimeTickFormatter(seconds= ["%M:%S"])
    plot.step("Time", "CoordP", source = source2, line_width = 2, mode = "after", line_color = "black", line_dash = "dashed")
    
    
    #plot.patch("Time", "CoordP", source = source2, fill_color = "orange", alpha = 0.8)
    #plot.patch("Time", "CoordM", source = source2, fill_color = "blue", alpha = 1.0)
    
    mbar = plot.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehovertmag, fill_color = "#315DFF", hover_fill_color = "cyan", line_color = "black", line_alpha = 0.8)
    pbar = plot.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehovertphys, fill_color = "#FFD00B", hover_fill_color = "firebrick", line_color = "black", line_alpha = 0.8)
    tbar = plot.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehovertrue, fill_color = "#E5E5E5", hover_fill_color = "gray", line_color = "black", line_alpha = 0.8)

    plot.add_tools(HoverTool(renderers = [mbar, pbar, tbar], tooltips="""
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
    ))
    
    
    
    #Extracting instances with CC
    CCs = df[df["CC"] != "None"]
    durations = df.CCDuration[df["CCDuration"] != 0]
    CCs = CCs.reset_index(drop = True)
    durations = durations.reset_index(drop = True)
    CCs["vari"] = np.zeros(len(CCs))
        
    #CC Indicator hell
    var = 1
    for count7 in range(len(CCs)):
        CCs.loc[count7, "vari"] = var
        if count7 - 1 >= 0:
        
            if CCs.Time[count7] <= CCs.Time[count7 - 1] + CCs.CCDuration[count7 - 1]:
                var = var + 1
                CCs.loc[count7, "vari"] = var
            if CCs.Time[count7] > CCs.Time[count7 - 1] + CCs.CCDuration[count7 - 1]:
                var = var - 1
                CCs.loc[count7, "vari"] = var
        if var <= 0:
            var = 1
            CCs.loc[count7, "vari"] = var
    CCs["vari"] = CCs["vari"] * -50
    CCsn = CCs[CCs["CCDuration"] != 0]
    CCsi = CCs[CCs["CCDuration"] == 0]
    CCsn = CCsn.reset_index(drop = True)
    CCsi = CCsi.reset_index(drop = True)
    CCTypes = {"Stun":"red", "Slow":"blue", "Knockup":"yellow", "Polymorph":"magenta", "Taunt":"green", "Knockback":"black", "Stasis":"orange"}
    ccc = []
    for count16 in range(len(CCsn)):
        ccc.append(CCTypes[CCsn.CC[count16]])
    
    
    
    source3 = ColumnDataSource(data = dict(x0 = CCsn.Time,
                                           y0 = CCsn.vari,
                                           x1 = CCsn.Time + CCsn.CCDuration,
                                           y1 = CCsn.vari,
                                           desc = CCsn.Champion + " - " + CCsn.Ability,
                                           img = CCsn.Image,
                                           linecolor = ccc,
                                           legend = CCsn.CC,
                                           dmg = CCsn.Total.astype(str) + " Damage",
                                           duration = CCsn.CCDuration / 1000
                                           ))
    ccsnbar = plot.segment(x0 = "x0", y0 = "y0", x1 = "x1", y1 = "y1", source = source3, line_color = "linecolor", line_width = 6, legend = "legend")
    plot.add_tools(HoverTool(renderers = [ccsnbar], tooltips="""
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
            <span style="font-size: 15px;">@legend - @duration seconds</span>
        </div>
    </div>
    """
    ))
    source5 = ColumnDataSource(data = dict(x0 = CCsn.Time,
                                           y0 = CCsn.vari,
                                           x1 = CCsn.Time + CCsn.CCDuration,
                                           y1 = CCsn.vari,
                                           desc = CCsn.Champion + " - " + CCsn.Ability,
                                           img = CCsn.CCImage,
                                           linecolor = ccc,
                                           legend = CCsn.CC,
                                           dmg = CCsn.Total.astype(str) + " Damage"
                                           ))
    width = (max(df.Time) - min(df.Time))/35
    
    image2 = ImageURL(x = "x0", y = "y0", url = "img", w = width, h = 50, anchor = "center")
    image3 = ImageURL(x = "x1", y = "y1", url = "img", w = width, h = 50, anchor = "center")
    plot.add_glyph(source5, image2)
    plot.add_glyph(source5, image3)
    
    source4 = ColumnDataSource(data = dict(x = CCsi.Time,
                                           y = CCsi.vari,
                                           desc = CCsi.Champion + " - " + CCsi.Ability,
                                           img = CCsi.Image,
                                           legend = CCsi.CC,
                                           dmg = CCsi.Total.astype(str) + " Damage",
                                           url = CCsi.CCImage
                                           ))
    ccsix = plot.x(x = "x", y = "y", source = source4, size = 6, line_color = "white", line_width = 4)
    plot.add_tools(HoverTool(renderers = [ccsix], tooltips="""
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
            <span style="font-size: 15px;">@legend</span>
        </div>
    </div>
    """
    ))
    image1 = ImageURL(url = "url",
                  x = "x",
                  y = "y",
                  w = .4,
                  h = 50,
                  anchor = "center")
    plot.add_glyph(source4, image1)
    plot.legend.background_fill_color = "lightgray"
    
    #Other plot
    
    plot2 = figure(x_axis_label = "Time", y_axis_label =  "Damage", title = "Damage by Type", tools = [hoverm])
    plot2.title.text_font = "times"
    plot2.xaxis.axis_label_text_font = "times"
    plot2.xaxis.axis_label_text_font_style = "bold"
    plot2.yaxis.axis_label_text_font = "times"
    plot2.yaxis.axis_label_text_font_style = "bold"
    
    plot2.step("Time", "cumulative_phys", source = source, line_width = 2, mode = "after", line_color = "#FFD00B")
    plot2.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehoverp, fill_color = "#FFD00B", hover_fill_color = "firebrick", legend = "Physical")
    
    plot2.step("Time", "cumulative_magic", source = source, line_width = 2, mode = "after", line_color = "#315DFF")
    plot2.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehoverm, fill_color = "#315DFF", hover_fill_color = "cyan", legend = "Magical")
               
    plot2.step("Time", "cumulative_true", source = source, line_width = 2, mode = "after", line_color = "gray")
    plot2.quad(top = "top", bottom = "bottom", left = "left", right = "right", source = sourcehovertt, fill_color = "#E5E5E5", hover_fill_color = "gray", legend = "True")
    plot2.legend.location = "top_left"
    plot2.legend.click_policy = "hide"
    
    
    
    #Using only relevant champions
    champinos = list(df.Champion.unique())
    plot3 = figure(x_axis_label = "Time", y_axis_label = "Damage", title = "Cumulative Damage by Champion", tools = [hoverm])
    plot3.title.text_font = "times"
    plot3.xaxis.axis_label_text_font = "times"
    plot3.xaxis.axis_label_text_font_style = "bold"
    plot3.yaxis.axis_label_text_font = "times"
    plot3.yaxis.axis_label_text_font_style = "bold"
    #Loop to plot each champ's damage
    for count6 in range(len(champinos)):
        #Name of columns
        name = "cumulative_" + champinos[count6]
        
        #Plot
        colors = {0: "red", 1: "blue", 2: "green", 3: "purple", 4: "black", 5: "cyan"}
        dfch = df[df["Champion"] == champinos[count6]]
        dfch["Right"] = dfch.Time + right
        dfch["Bottom"] = dfch[name] - dfch.Total
        sourcech = ColumnDataSource(data = dict(top = dfch[name],
                                               left = dfch.Time,
                                               right = dfch.Right,
                                               bottom = dfch.Bottom,
                                               img = dfch.Image,
                                               desc = dfch.Champion + " - " + dfch.Ability,
                                               dmg = dfch.Total.astype(str) + " Damage"))
        
        plot3.step("Time", name, source = source, mode = "after", legend = champinos[count6], color = colors[count6])
        plot3.quad(top = "top", left = "left", bottom = "bottom", right = "right", source = sourcech, fill_color = colors[count6], hover_fill_color = "gray", legend = champinos[count6])
    plot3.legend.location = "top_left"
    plot3.legend.click_policy = "hide"


    champoninos = list(df.Champion.unique())
    champoninos = sorted(champoninos)
    types = ["Magical", "Physical", "True"]
    colors = ["#315DFF", "#FFD00B", "#E5E5E5"]
    
    
    
    
    bplot = figure(x_range = champoninos, x_axis_label = "Champions", y_axis_label = "Damage", tools = [], plot_width = 700, plot_height = 600)
    bplot.title.text_font = "times"
    bplot.xaxis.axis_label_text_font = "arial"
    bplot.xaxis.axis_label_text_font_style = "bold"
    bplot.xaxis.axis_label_text_font_size = "16pt"
    bplot.yaxis.axis_label_text_font = "arial"
    bplot.yaxis.axis_label_text_font_style = "bold"
    bplot.yaxis.axis_label_text_font_size = "16pt"
    bplot.xaxis.major_label_text_font_size = "10pt"
    bplot.yaxis.major_label_text_font_size = "10pt"
    
    for count18 in range(len(champoninos)):
        newdf = df[df["Champion"] == champoninos[count18]]
        magical = newdf[newdf["Type"] == "Magical"]
        physical = newdf[newdf["Type"] == "Physical"]
        true = newdf[newdf["Type"] == "True"]
        magical = magical.groupby(["Ability", "Image"]).agg({"Total":"sum"})
        physical = physical.groupby(["Ability", "Image"]).agg({"Total":"sum"})
        true = true.groupby(["Ability", "Image"]).agg({"Total":"sum"})
        magical = magical.reset_index(drop = False)
        physical = physical.reset_index(drop = False)
        true = true.reset_index(drop = False)
        magical["Type"] = "Magical"
        physical["Type"] = "Physical"
        true["Type"] = "True"
        shades = {"Magical" : "#315DFF", "Physical" : "#FFD00B", "True" : "#E5E5E5"}
        
        reorg = pd.concat([magical, physical, true], axis = 0)
        reorg = reorg.reset_index(drop = True)
        reorg["bot"] = np.zeros(len(reorg))
        reorg["top"] = np.zeros(len(reorg))
        reorg["color"] = np.zeros(len(reorg))
        reorg["Champion"] = champoninos[count18]
        prev = 0
        for count19 in range(len(reorg)):
            reorg.loc[count19, "bot"] = prev
            reorg.loc[count19, "top"] = prev + reorg["Total"][count19]
            prev = reorg.loc[count19, "top"]
            reorg.loc[count19, "color"] = shades[reorg["Type"][count19]]
        for count20 in range(len(reorg)):
            pleasework = ColumnDataSource(data = dict(Champion = reorg.Champion,
                                                      Total = reorg.Total,
                                                      top = reorg.top,
                                                      bot = reorg.bot,
                                                      color = reorg.color,
                                                      img = reorg.Image,
                                                      desc = reorg.Champion + " - " + reorg.Ability,
                                                      dmg = reorg.Total.astype(str) + " Damage"))
            bplot.vbar(source = pleasework, x = "Champion", width = 0.9, bottom = "bot", top = "top", color = "color", line_color = "black", line_alpha = 0.4, hover_fill_color = "firebrick")
        pleasehover = hoverm
        bplot.add_tools(pleasehover)
        
    
    
    
    
    
    bplot.y_range.start = 0
    bplot.x_range.range_padding = 0.1
    bplot.xgrid.grid_line_color = None
    bplot.axis.minor_tick_line_color = None
    bplot.outline_line_color = None
    bplot.legend.location = "top_left"
    bplot.legend.orientation = "horizontal"  
    
    '''tab1 = Panel(child = plot, title = "Overall Damage")
    tab2 = Panel(child = plot2, title = "Damage by Type")
    tab3 = Panel(child = plot3, title = "Damage by Champion")
    tab4 = Panel(child = bplot, title = "Bar")
    layout = Tabs(tabs = [tab1, tab2, tab3, tab4])'''
    output_file("wait_this_works" + str(fightid) + ".html")
    #plot.sizing_mode = "scale_both"
    #bplot.sizing_mode = "scale_both"
    layout1 = row([bplot, plot], sizing_mode = "scale_both")
    layout2 = layout([[bplot, plot]], sizing_mode = "scale_both")
    #curdoc().add_root(layout2)
    show(layout([[Div(text = "<h1>Death Recap</h1>")], [bplot, plot]], sizing_mode = "fixed"))
    
    
    
    
    
    
    
    
    
    
    
    