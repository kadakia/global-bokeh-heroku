
# coding: utf-8

# In[87]:

from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Button, RadioGroup, Toggle, CheckboxGroup, Select, Slider, Panel, Tabs, CategoricalColorMapper
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.palettes import Spectral6
# from bokeh.charts import BoxPlot, Histogram
# import holoviews as hv
# hv.extension('bokeh')

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


# In[121]:

import numpy as np
#from math import pi


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


# In[122]:

# Make a slider object
slider_2 = Slider(start = 1970, end = 1980, step = 10, value = 1970, title = 'Year')

# find the quartiles and IQR for each category
groups = data.loc[1970].groupby('region')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# find the outliers for each category
def outliers(group):
    cat = group.name
    return group[(group.life > upper.loc[cat]['life']) | (group.life < lower.loc[cat]['life'])]['life']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in list(data['region'].unique()):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)
                
p = figure(background_fill_color="#EFE8E2", title="", x_range=list(data['region'].unique()))
p.xaxis.major_label_orientation = pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]

# stems
p.segment(list(data['region'].unique()), upper.life, list(data['region'].unique()), q3.life, line_color="black")
p.segment(list(data['region'].unique()), lower.life, list(data['region'].unique()), q1.life, line_color="black")

# boxes
p.vbar(list(data['region'].unique()), 0.7, q2.life, q3.life, fill_color="#E08E79", line_color="black")
p.vbar(list(data['region'].unique()), 0.7, q1.life, q2.life, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p.rect(list(data['region'].unique()), lower.life, 0.2, 0.01, line_color="black")
p.rect(list(data['region'].unique()), upper.life, 0.2, 0.01, line_color="black")

# outliers
# if not out.empty:
#     p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="10pt"

# Define the callback function
def update_plot(attr, old, new):
    if slider_2.value == 1970:
        # find the quartiles and IQR for each category
        groups = data.loc[1970].groupby('region')
        q1 = groups.quantile(q=0.25)
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75)
        iqr = q3 - q1
        upper = q3 + 1.5*iqr
        lower = q1 - 1.5*iqr

        # find the outliers for each category
        def outliers(group):
            cat = group.name
            return group[(group.life > upper.loc[cat]['life']) | (group.life < lower.loc[cat]['life'])]['life']
        out = groups.apply(outliers).dropna()

        # prepare outlier data for plotting, we need coordinates for every outlier.
        if not out.empty:
            outx = []
            outy = []
            for cat in list(data['region'].unique()):
                # only add outliers if they exist
                if not out.loc[cat].empty:
                    for value in out[cat]:
                        outx.append(cat)
                        outy.append(value)
  
        p = figure(background_fill_color="#EFE8E2", title="", x_range=list(data['region'].unique()))
        p.xaxis.major_label_orientation = pi/2

        # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
        lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]

        # stems
        p.segment(list(data['region'].unique()), upper.life, list(data['region'].unique()), q3.life, line_color="black")
        p.segment(list(data['region'].unique()), lower.life, list(data['region'].unique()), q1.life, line_color="black")

        # boxes
        p.vbar(list(data['region'].unique()), 0.7, q2.life, q3.life, fill_color="#E08E79", line_color="black")
        p.vbar(list(data['region'].unique()), 0.7, q1.life, q2.life, fill_color="#3B8686", line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect(list(data['region'].unique()), lower.life, 0.2, 0.01, line_color="black")
        p.rect(list(data['region'].unique()), upper.life, 0.2, 0.01, line_color="black")

        # outliers
        # if not out.empty:
        #     p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size="10pt"
    elif slider_2.value == 1980:
        # find the quartiles and IQR for each category
        groups = data.loc[1980].groupby('region')
        q1 = groups.quantile(q=0.25)
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75)
        iqr = q3 - q1
        upper = q3 + 1.5*iqr
        lower = q1 - 1.5*iqr

        # find the outliers for each category
        def outliers(group):
            cat = group.name
            return group[(group.life > upper.loc[cat]['life']) | (group.life < lower.loc[cat]['life'])]['life']
        out = groups.apply(outliers).dropna()

        # prepare outlier data for plotting, we need coordinates for every outlier.
        if not out.empty:
            outx = []
            outy = []
            for cat in list(data['region'].unique()):
                # only add outliers if they exist
                if not out.loc[cat].empty:
                    for value in out[cat]:
                        outx.append(cat)
                        outy.append(value)
  
        p = figure(background_fill_color="#EFE8E2", title="", x_range=list(data['region'].unique()))
        p.xaxis.major_label_orientation = pi/2

        # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
        lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]

        # stems
        p.segment(list(data['region'].unique()), upper.life, list(data['region'].unique()), q3.life, line_color="black")
        p.segment(list(data['region'].unique()), lower.life, list(data['region'].unique()), q1.life, line_color="black")

        # boxes
        p.vbar(list(data['region'].unique()), 0.7, q2.life, q3.life, fill_color="#E08E79", line_color="black")
        p.vbar(list(data['region'].unique()), 0.7, q1.life, q2.life, fill_color="#3B8686", line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect(list(data['region'].unique()), lower.life, 0.2, 0.01, line_color="black")
        p.rect(list(data['region'].unique()), upper.life, 0.2, 0.01, line_color="black")

        # outliers
        # if not out.empty:
        #     p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size="10pt"
        
    
# Attach the callback to the 'value' property of slider
slider_2.on_change('value', update_plot)

#layout = row(widgetbox(slider_2), p)



# Make the ColumnDataSource
source = ColumnDataSource(data={
                          'x'       : data.loc[1970].fertility,
                          'y'       : data.loc[1970].life,
                          'country'      : data.loc[1970].Country,
                          #    'pop'      : (data.loc[1970].population / 20000000) + 2,
                          'region'      : data.loc[1970].region
                          })

# Save the minimum and maximum values of the fertility column
xmin, xmax = min(data.fertility), max(data.fertility)

# Save the minimum and maximum values of the life expectancy column
ymin, ymax = min(data.life), max(data.life)

# Create the figure
plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Add circle glyphs to the plot
# plot.circle(x='x', y='y', fill_alpha=0.8, source=source_2)

# Set the x-axis label
plot.xaxis.axis_label ='fertility'

# Set the y-axis label
plot.yaxis.axis_label = 'life'

# Add the plot to the current document and add a title
# curdoc().add_root(plot)
# curdoc().title = 'Gapminder'

# output_file('gapminder_2.html')
# show(plot)

# Make a list of the unique values from the region column
regions_list = data.region.unique().tolist()

# Make a color mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# output_file('gapminder_2.html')
# show(plot)

# Make a slider object
slider = Slider(start = 1970, end = 2010, step = 1, value = 1970, title = 'Year')

# Define the callback function
def update_plot_2(attr, old, new):
    
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        #        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region
    }
    source.data = new_data

# Set the range of all axes
plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])
    
    # Add title to figure
    plot.title.text = 'Gapminder data for %d' % yr

# Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

# Set the legend.location attribute of the plot
plot.legend.location = 'bottom_left'

# Attach the callback to the 'value' property of slider
slider.on_change('value',update_plot_2)

# Create a HoverTool
hover = HoverTool(tooltips = [('Country', '@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)

# Create a dropdown Select widget for the x data
x_select = Select(
                  options=['fertility', 'life', 'child_mortality', 'gdp'],
                  value='fertility',
                  title='x-axis data'
                  )

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot_2)

# Create a dropdown Select widget for the y data
y_select = Select(
                  options=['fertility', 'life', 'child_mortality'],
                  value='life',
                  title='y-axis data'
                  )

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot_2)

#layout = row(widgetbox(slider,x_select,y_select), plot)

# output_file('gapminder.html')
# show(layout)
#curdoc().add_root(layout)


tab1 = Panel(child=row(widgetbox(slider,x_select,y_select), plot), title='Interactive Scatter')

tab2 = Panel(child=row(widgetbox(slider_2), p), title='Box Plots')

layout = Tabs(tabs=[tab1, tab2])


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


# In[120]:

# hist_1970 = Histogram(data.loc[1970], values = 'life', color='region', legend='top_left')
# hist_2000 = Histogram(data.loc[2000], values = 'life', color='region', legend='top_left')

# tab1 = Panel(child=hist_1970, title='Life Expectancy in 1970')

# tab2 = Panel(child=hist_2000, title='Life Expectancy in 2000')

# layout = Tabs(tabs=[tab1,tab2])

# curdoc().add_root(layout)
# output_notebook()
# show(layout)


