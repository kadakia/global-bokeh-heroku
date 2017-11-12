
# coding: utf-8

# In[127]:

from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Button, RadioGroup, Toggle, CheckboxGroup, Select, Slider, Panel, Tabs, CategoricalColorMapper
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.palettes import Spectral6
# from bokeh.charts import BoxPlot, Histogram
# import holoviews as hv
# hv.extension('bokeh')
# import matplotlib.pyplot as plt
# import seaborn as sns

# from bokeh.server.server import Server
# from bokeh.embed import autoload_server
# from bokeh.client import push_session


# In[83]:

import pandas as pd

data = pd.read_csv('gapminder_tidy.csv', index_col = 'Year')

print(data['region'].value_counts())
print(data.columns)
print(data.info())

# data_Eur = data[data['region'] == 'Europe & Central Asia']
# data_Sub = data[data['region'] == 'Sub-Saharan Africa']
# data_Ame = data[data['region'] == 'America']
# data_Eas = data[data['region'] == 'East Asia & Pacific']
# data_Mid = data[data['region'] == 'Middle East & North Africa']
# data_Sou = data[data['region'] == 'South Asia']


# In[187]:

import numpy as np
# from math import pi



# In[119]:

# Make the ColumnDataSource
# source = ColumnDataSource(data={
#                           'x'      : data.loc[1970].region,
#                           'y'       : data.loc[1970].life,
#                           'country' : data.loc[1970].Country
#                           })


# Save the minimum and maximum values of the life expectancy column
# ymin, ymax = min(data.life), max(data.life)


# box = BoxPlot(data.loc[1970], values = 'life', label='region', color = 'region', legend=False, title='Boxplots by region, 1970')
# plot_height=400, plot_width=700


# Set the x-axis label
# box.xaxis.axis_label = 'region'

# Set the y-axis label
# box.yaxis.axis_label = 'life'


# curdoc().add_root(box)
# output_notebook()
# show(box)
    

# box_fert = BoxPlot(data.loc[2000], values='fertility', label='region', color = 'region', legend=False)

# tab1 = Panel(child=box_life, title='Life Expectancy')

# tab2 = Panel(child=box_fert, title='Fertility')

# layout = Tabs(tabs=[tab1,tab2])

# curdoc().add_root(layout)
# output_notebook()
# show(layout)

# box = sns.boxplot(x = 'region', y = 'life',data = data.loc[1970])
# plt.setp(box.get_xticklabels(), rotation=90)
# plt.show()




# Define the callback function
# def update_plot(attr, old, new):
    
#     yr = slider_2.value
#     x = 'region'
#     y = y_select.value
    
    # Label axes of plot
#     box.xaxis.axis_label = 'region'
#     box.yaxis.axis_label = y

#     new_data = {
#         'x'       : data.loc[yr][x],
#         'y'       : data.loc[yr][y],
#         'country' : data.loc[yr].Country,
#         'region'  : data.loc[yr].region
#     }
#     source.data = new_data

# Set the range of all axes
#    plot.x_range.start = min(data[x])
#    plot.x_range.end = max(data[x])
#    plot.y_range.start = min(data[y])
#    plot.y_range.end = max(data[y])
    
    # Add title to figure
#     box.title.text = 'Boxplots by region, %d' % yr
    
# yr = slider.value
# y = y_select.value
    
# Add the color mapper to the circle glyph
# box = BoxPlot(data.loc[yr], values = y, source=source, label='region', color = 'region', legend=False, title = 'Boxplots by region, %d' % yr)

# box.xaxis.axis_label = 'region'
# box.yaxis.axis_label = y

# Attach the callback to the 'value' property of slider
# slider_2.on_change('value', update_plot)

# Create a dropdown Select widget for the y data
# y_select = Select(
#                   options=['fertility', 'life', 'child_mortality', 'gdp'],
#                   value='fertility',
#                   title='y-axis data'
#                   )

# Attach the update_plot callback to the 'value' property of y_select
# y_select.on_change('value', update_plot)


# layout = row(widgetbox(slider,y_select), box)

# curdoc().add_root(layout)
# output_notebook()
# show(layout)


# In[199]:

groups = data.loc[1970].groupby('region')

q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# Make the ColumnDataSource
source_2 = ColumnDataSource(data={
                          'x'       : sorted(list(data['region'].unique())),
                          'y'       : data.loc[1970].life,
#                          'region'      : data.loc[1970].region
                          })

    
p = figure(background_fill_color="#EFE8E2", title="Boxplots by region, 1970", x_range=sorted(list(data['region'].unique())))
p.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]
#p.y_range.start = min(data['life'])
#p.y_range.end = max(data['life'])

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="10pt"

p.xaxis.axis_label = 'region'
p.yaxis.axis_label = 'life'


# Make a slider object
slider_2 = Slider(start = 1970, end = 2010, step = 1, value = 1970, title = 'Year')

# Create a dropdown Select widget for the y data
y_select = Select(
                  options=['fertility', 'life', 'child_mortality', 'gdp'],
                  value='life',
                  title='y-axis data'
                  )

if y_select.value == 'life':
    upper_y = upper['life']
elif y_select.value == 'fertility':
    upper_y = upper['fertility']
elif y_select.value == 'child_mortality':
    upper_y = upper['child_mortality']
elif y_select.value == 'gdp':
    upper_y = upper['gdp']
    
if y_select.value == 'life':
    lower_y = lower['life']
elif y_select.value == 'fertility':
    lower_y = lower['fertility']
elif y_select.value == 'child_mortality':
    lower_y = lower['child_mortality']
elif y_select.value == 'gdp':
    lower_y = lower['gdp']
    
if y_select.value == 'life':
    q1_y = q1['life']
elif y_select.value == 'fertility':
    q1_y = q1['fertility']
elif y_select.value == 'child_mortality':
    q1_y = q1['child_mortality']
elif y_select.value == 'gdp':
    q1_y = q1['gdp']
    
if y_select.value == 'life':
    q2_y = q2['life']
elif y_select.value == 'fertility':
    q2_y = q2['fertility']
elif y_select.value == 'child_mortality':
    q2_y = q2['child_mortality']
elif y_select.value == 'gdp':
    q2_y = q2['gdp']
    
if y_select.value == 'life':
    q3_y = q3['life']
elif y_select.value == 'fertility':
    q3_y = q3['fertility']
elif y_select.value == 'child_mortality':
    q3_y = q3['child_mortality']
elif y_select.value == 'gdp':
    q3_y = q3['gdp']


# Define the callback function
def update_plot(attr, old, new):
    
    yr = slider_2.value
    # find the quartiles and IQR for each category
    groups = data.loc[yr].groupby('region')
#    x = x_select.value
    y = y_select.value
    
    # Label axes of plot
#    p.xaxis.axis_label = x
    p.yaxis.axis_label = y

    new_data = {
#        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
#        'region'  : data.loc[yr].region
    }
    source_2.data = new_data

    # Set the range of all axes
#    p.x_range.start = min(data[x])
#    p.x_range.end = max(data[x])
    p.y_range.start = min(data[y])
    p.y_range.end = max(data[y])
    #qmin = groups.quantile(q=0.00)
    #qmax = groups.quantile(q=1.00)
    #upper[y] = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,y]),upper[y])]
    #lower[y] = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,y]),lower[y])]
    
    # Add title to figure
    p.title.text = 'Boxplots by region, for %d' % yr
    

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)


# find the outliers for each category
#def outliers(group):
#    cat = group.name
#    if y_select.value == 'life':
#        group_y = group['life']
#    elif y_select.value == 'fertility':
#        group_y = group['fertility']
#    elif y_select.value == 'child_mortality':
#        group_y = group['child_mortality']
#    elif y_select.value == 'gdp':
#        group_y = group['gdp']
#    return group[(group['y'] > upper.loc[cat]['y']) | (group['y'] < lower.loc[cat]['y'])]['y']
#out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
#if not out.empty:
#    outx = []
#    outy = []
#    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
#        if not out.loc[cat].empty:
#            for value in out[cat]:
#                outx.append(cat)
#                outy.append(value)

# stems
p.segment('x', upper_y, 'x', q3_y, line_color="black")
p.segment('x', lower_y, 'x', q1_y, line_color="black")

# boxes
p.vbar('x', 0.7, q2_y, q3_y, fill_color="#E08E79", line_color="black")
p.vbar('x', 0.7, q1_y, q2_y, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p.rect('x', upper_y, width = 0.2, height = 0.01, line_color="black", source = source_2)
p.rect('x', lower_y, width = 0.2, height = 0.01, line_color="black")

# outliers
#if not out.empty:
#    p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
    

# Attach the callback to the 'value' property of slider
slider_2.on_change('value', update_plot)


layout = row(widgetbox(slider,y_select), p)

curdoc().add_root(layout)
output_notebook()
show(layout)


# In[120]:

# hist_1970 = Histogram(data.loc[1970], values = 'life', color='region', legend='top_left')
# hist_2000 = Histogram(data.loc[2000], values = 'life', color='region', legend='top_left')

# tab1 = Panel(child=hist_1970, title='Life Expectancy in 1970')

# tab2 = Panel(child=hist_2000, title='Life Expectancy in 2000')

# layout = Tabs(tabs=[tab1,tab2])

# curdoc().add_root(layout)
# output_notebook()
# show(layout)


