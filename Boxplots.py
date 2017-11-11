
# coding: utf-8

# In[82]:

from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Button, RadioGroup, Toggle, CheckboxGroup, Select, Slider, Panel, Tabs, CategoricalColorMapper
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.palettes import Spectral6
# from bokeh.charts import BoxPlot, Histogram
import holoviews as hv
hv.extension('bokeh')

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


# In[84]:

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


# In[86]:

# Make a slider object
slider_2 = Slider(start = 1970, end = 1971, step = 1, value = 1970, title = 'Year')

    
# Define the callback function
def update_plot(attr, old, new):
    if slider_2.value == 1970:
    #   box = BoxPlot(data.loc[1970], values = 'life', label='region', color = 'region', legend=False, title='Boxplots by region, 1970')
        box = hv.BoxWhisker(data.loc[1970], ['region'], 'life', label = 'Boxplots by region, 1970')
        plot_opts = dict(show_legend=False)
        style = dict(color='region')
        box(plot=plot_opts, style=style)
    elif slider_2.value == 1971:
    #   box = BoxPlot(data.loc[1971], values = 'life', label='region', color = 'region', legend=False, title='Boxplots by region, 1971')
        box = hv.BoxWhisker(data.loc[1971], ['region'], 'life', label = 'Boxplots by region, 1971')
        plot_opts = dict(show_legend=False)
        style = dict(color='region')
        box(plot=plot_opts, style=style)

# Attach the callback to the 'value' property of slider
slider_2.on_change('value', update_plot)
    
    
layout = row(widgetbox(slider_2), box)

curdoc().add_root(layout)
output_notebook()
show(layout)


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


# In[49]:

# hist_1970 = Histogram(data.loc[1970], values = 'life', color='region', legend='top_left')
# hist_2000 = Histogram(data.loc[2000], values = 'life', color='region', legend='top_left')

# tab1 = Panel(child=hist_1970, title='Life Expectancy in 1970')

# tab2 = Panel(child=hist_2000, title='Life Expectancy in 2000')

# layout = Tabs(tabs=[tab1,tab2])

# curdoc().add_root(layout)
# output_notebook()
# show(layout)

