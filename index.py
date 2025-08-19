
# coding: utf-8

# In[87]:

from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import TextInput, HoverTool, Button, RadioGroup, Toggle, CheckboxGroup, Select, Slider, Panel, Tabs, CategoricalColorMapper
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

data_Eur = data[data['region'] == 'Europe & Central Asia']
data_Sub = data[data['region'] == 'Sub-Saharan Africa']
data_Ame = data[data['region'] == 'America']
data_Eas = data[data['region'] == 'East Asia & Pacific']
data_Mid = data[data['region'] == 'Middle East & North Africa']
data_Sou = data[data['region'] == 'South Asia']
data_US = data[data['Country'] == 'United States'].reset_index()
data_Haiti = data[data['Country'] == 'Haiti'].reset_index()
data_China = data[data['Country'] == 'China'].reset_index()

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
# slider_2 = Slider(start = 1970, end = 1980, step = 10, value = 1970, title = 'Year')

#LIFE EXPECTANCY

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
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)
                
p = figure(background_fill_color="#EFE8E2", title="Life expectancy by region, 1970", x_range=sorted(list(data['region'].unique())))
p.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]

p.y_range.start = 30
p.y_range.end = 90

# stems
p.segment(sorted(list(data['region'].unique())), upper.life, sorted(list(data['region'].unique())), q3.life, line_color="black")
p.segment(sorted(list(data['region'].unique())), lower.life, sorted(list(data['region'].unique())), q1.life, line_color="black")

# boxes
p.vbar(sorted(list(data['region'].unique())), 0.7, q2.life, q3.life, fill_color="#E08E79", line_color="black")
p.vbar(sorted(list(data['region'].unique())), 0.7, q1.life, q2.life, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p.rect(sorted(list(data['region'].unique())), lower.life, 0.2, 0.01, line_color="black")
p.rect(sorted(list(data['region'].unique())), upper.life, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="10pt"

p.xaxis.axis_label = 'region'
p.yaxis.axis_label = 'life expectancy'



# find the quartiles and IQR for each category
groups = data.loc[2010].groupby('region')
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
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)
  
p_2010 = figure(background_fill_color="#EFE8E2", title="Life expectancy by region, 2010", x_range=sorted(list(data['region'].unique())))
p_2010.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.life = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'life']),upper.life)]
lower.life = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'life']),lower.life)]

p_2010.y_range.start = 30
p_2010.y_range.end = 90

# stems
p_2010.segment(sorted(list(data['region'].unique())), upper.life, sorted(list(data['region'].unique())), q3.life, line_color="black")
p_2010.segment(sorted(list(data['region'].unique())), lower.life, sorted(list(data['region'].unique())), q1.life, line_color="black")

# boxes
p_2010.vbar(sorted(list(data['region'].unique())), 0.7, q2.life, q3.life, fill_color="#E08E79", line_color="black")
p_2010.vbar(sorted(list(data['region'].unique())), 0.7, q1.life, q2.life, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_2010.rect(sorted(list(data['region'].unique())), lower.life, 0.2, 0.01, line_color="black")
p_2010.rect(sorted(list(data['region'].unique())), upper.life, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_2010.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_2010.xgrid.grid_line_color = None
p_2010.ygrid.grid_line_color = "white"
p_2010.grid.grid_line_width = 2
p_2010.xaxis.major_label_text_font_size="10pt"

p_2010.xaxis.axis_label = 'region'
p_2010.yaxis.axis_label = 'life expectancy'


# Attach the callback to the 'value' property of slider
# slider_2.on_change('value', update_plot)

#layout = row(widgetbox(slider_2), p)


#INTERACTIVE SCATTER

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
plot = figure(title='Gapminder data for 1970', plot_height=400, plot_width=700,
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

# Create a Button with label 'Update Data'
button = Button(label='Freeze Frame: America')

# Define an update callback with no arguments: update
def update():
    
    yr = slider.value
    x = x_select.value
    y = y_select.value
    
    # Update the ColumnDataSource data dictionary
    source.data = {'x': data_Ame.loc[yr][x], 'y': data_Ame.loc[yr][y], 'country' : data_Ame.loc[yr].Country, 'region'  : data_Ame.loc[yr].region}

# Add the update callback to the button
button.on_click(update)


# Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')


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


# Set the legend.location attribute of the plot
# if y_select.value == 'life' and x_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'
# elif y_select.value == 'life' and x_select.value == 'gdp':
#     plot.legend.location = 'bottom_right'
# elif y_select.value == 'life' and x_select.value == 'child_mortality':
#     plot.legend.location = 'top_right'
# elif y_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'
# elif y_select.value == 'child_mortality' and x_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'

plot.legend.location = 'bottom_left'

plot.legend.click_policy="hide"

# Attach the callback to the 'value' property of slider
slider.on_change('value',update_plot_2)

# Create a HoverTool
hover = HoverTool(tooltips = [('Country', '@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)

#layout = row(widgetbox(slider,x_select,y_select), plot)

# output_file('gapminder.html')
# show(layout)
#curdoc().add_root(layout)

#FERTILITY


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
    return group[(group.fertility > upper.loc[cat]['fertility']) | (group.fertility < lower.loc[cat]['fertility'])]['fertility']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_fert = figure(background_fill_color="#EFE8E2", title="Fertility by region, 1970", x_range=sorted(list(data['region'].unique())))
p_fert.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.fertility = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'fertility']),upper.fertility)]
lower.fertility = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'fertility']),lower.fertility)]

p_fert.y_range.start = 0
p_fert.y_range.end = 9

# stems
p_fert.segment(sorted(list(data['region'].unique())), upper.fertility, sorted(list(data['region'].unique())), q3.fertility, line_color="black")
p_fert.segment(sorted(list(data['region'].unique())), lower.fertility, sorted(list(data['region'].unique())), q1.fertility, line_color="black")

# boxes
p_fert.vbar(sorted(list(data['region'].unique())), 0.7, q2.fertility, q3.fertility, fill_color="#E08E79", line_color="black")
p_fert.vbar(sorted(list(data['region'].unique())), 0.7, q1.fertility, q2.fertility, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_fert.rect(sorted(list(data['region'].unique())), lower.fertility, 0.2, 0.01, line_color="black")
p_fert.rect(sorted(list(data['region'].unique())), upper.fertility, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_fert.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_fert.xgrid.grid_line_color = None
p_fert.ygrid.grid_line_color = "white"
p_fert.grid.grid_line_width = 2
p_fert.xaxis.major_label_text_font_size="10pt"

p_fert.xaxis.axis_label = 'region'
p_fert.yaxis.axis_label = 'fertility'




# find the quartiles and IQR for each category
groups = data.loc[2010].groupby('region')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# find the outliers for each category
def outliers(group):
    cat = group.name
    return group[(group.fertility > upper.loc[cat]['fertility']) | (group.fertility < lower.loc[cat]['fertility'])]['fertility']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_fert_2010 = figure(background_fill_color="#EFE8E2", title="Fertility by region, 2010", x_range=sorted(list(data['region'].unique())))
p_fert_2010.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.fertility = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'fertility']),upper.fertility)]
lower.fertility = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'fertility']),lower.fertility)]

p_fert_2010.y_range.start = 0
p_fert_2010.y_range.end = 9

# stems
p_fert_2010.segment(sorted(list(data['region'].unique())), upper.fertility, sorted(list(data['region'].unique())), q3.fertility, line_color="black")
p_fert_2010.segment(sorted(list(data['region'].unique())), lower.fertility, sorted(list(data['region'].unique())), q1.fertility, line_color="black")

# boxes
p_fert_2010.vbar(sorted(list(data['region'].unique())), 0.7, q2.fertility, q3.fertility, fill_color="#E08E79", line_color="black")
p_fert_2010.vbar(sorted(list(data['region'].unique())), 0.7, q1.fertility, q2.fertility, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_fert_2010.rect(sorted(list(data['region'].unique())), lower.fertility, 0.2, 0.01, line_color="black")
p_fert_2010.rect(sorted(list(data['region'].unique())), upper.fertility, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_fert_2010.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_fert_2010.xgrid.grid_line_color = None
p_fert_2010.ygrid.grid_line_color = "white"
p_fert_2010.grid.grid_line_width = 2
p_fert_2010.xaxis.major_label_text_font_size="10pt"

p_fert_2010.xaxis.axis_label = 'region'
p_fert_2010.yaxis.axis_label = 'fertility'


#GDP


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
    return group[(group.gdp > upper.loc[cat]['gdp']) | (group.gdp < lower.loc[cat]['gdp'])]['gdp']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_gdp = figure(background_fill_color="#EFE8E2", title="GDP per capita by region, 1970", x_range=sorted(list(data['region'].unique())))
p_gdp.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.gdp = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'gdp']),upper.gdp)]
lower.gdp = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'gdp']),lower.gdp)]

# p_gdp.y_range.start = -2000
# p_gdp.y_range.end = 160000

# stems
p_gdp.segment(sorted(list(data['region'].unique())), upper.gdp, sorted(list(data['region'].unique())), q3.gdp, line_color="black")
p_gdp.segment(sorted(list(data['region'].unique())), lower.gdp, sorted(list(data['region'].unique())), q1.gdp, line_color="black")

# boxes
p_gdp.vbar(sorted(list(data['region'].unique())), 0.7, q2.gdp, q3.gdp, fill_color="#E08E79", line_color="black")
p_gdp.vbar(sorted(list(data['region'].unique())), 0.7, q1.gdp, q2.gdp, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_gdp.rect(sorted(list(data['region'].unique())), lower.gdp, 0.2, 0.01, line_color="black")
p_gdp.rect(sorted(list(data['region'].unique())), upper.gdp, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_gdp.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_gdp.xgrid.grid_line_color = None
p_gdp.ygrid.grid_line_color = "white"
p_gdp.grid.grid_line_width = 2
p_gdp.xaxis.major_label_text_font_size="10pt"

p_gdp.xaxis.axis_label = 'region'
p_gdp.yaxis.axis_label = 'gdp per capita'




# find the quartiles and IQR for each category
groups = data.loc[2010].groupby('region')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# find the outliers for each category
def outliers(group):
    cat = group.name
    return group[(group.gdp > upper.loc[cat]['gdp']) | (group.gdp < lower.loc[cat]['gdp'])]['gdp']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_gdp_2010 = figure(background_fill_color="#EFE8E2", title="GDP per capita by region, 2010", x_range=sorted(list(data['region'].unique())))
p_gdp_2010.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.gdp = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'gdp']),upper.gdp)]
lower.gdp = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'gdp']),lower.gdp)]

# p_gdp_2010.y_range.start = -2000
# p_gdp_2010.y_range.end = 160000

# stems
p_gdp_2010.segment(sorted(list(data['region'].unique())), upper.gdp, sorted(list(data['region'].unique())), q3.gdp, line_color="black")
p_gdp_2010.segment(sorted(list(data['region'].unique())), lower.gdp, sorted(list(data['region'].unique())), q1.gdp, line_color="black")

# boxes
p_gdp_2010.vbar(sorted(list(data['region'].unique())), 0.7, q2.gdp, q3.gdp, fill_color="#E08E79", line_color="black")
p_gdp_2010.vbar(sorted(list(data['region'].unique())), 0.7, q1.gdp, q2.gdp, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_gdp_2010.rect(sorted(list(data['region'].unique())), lower.gdp, 0.2, 0.01, line_color="black")
p_gdp_2010.rect(sorted(list(data['region'].unique())), upper.gdp, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_gdp_2010.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_gdp_2010.xgrid.grid_line_color = None
p_gdp_2010.ygrid.grid_line_color = "white"
p_gdp_2010.grid.grid_line_width = 2
p_gdp_2010.xaxis.major_label_text_font_size="10pt"

p_gdp_2010.xaxis.axis_label = 'region'
p_gdp_2010.yaxis.axis_label = 'gdp per capita'


#CHILD MORTALITY


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
    return group[(group.child_mortality > upper.loc[cat]['child_mortality']) | (group.child_mortality < lower.loc[cat]['child_mortality'])]['child_mortality']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_mort = figure(background_fill_color="#EFE8E2", title="Child mortality by region, 1970", x_range=sorted(list(data['region'].unique())))
p_mort.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.child_mortality = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'child_mortality']),upper.child_mortality)]
lower.child_mortality = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'child_mortality']),lower.child_mortality)]

p_mort.y_range.start = 0
p_mort.y_range.end = 400

# stems
p_mort.segment(sorted(list(data['region'].unique())), upper.child_mortality, sorted(list(data['region'].unique())), q3.child_mortality, line_color="black")
p_mort.segment(sorted(list(data['region'].unique())), lower.child_mortality, sorted(list(data['region'].unique())), q1.child_mortality, line_color="black")

# boxes
p_mort.vbar(sorted(list(data['region'].unique())), 0.7, q2.child_mortality, q3.child_mortality, fill_color="#E08E79", line_color="black")
p_mort.vbar(sorted(list(data['region'].unique())), 0.7, q1.child_mortality, q2.child_mortality, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_mort.rect(sorted(list(data['region'].unique())), lower.child_mortality, 0.2, 0.01, line_color="black")
p_mort.rect(sorted(list(data['region'].unique())), upper.child_mortality, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_mort.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_mort.xgrid.grid_line_color = None
p_mort.ygrid.grid_line_color = "white"
p_mort.grid.grid_line_width = 2
p_mort.xaxis.major_label_text_font_size="10pt"

p_mort.xaxis.axis_label = 'region'
p_mort.yaxis.axis_label = 'child mortality'



# find the quartiles and IQR for each category
groups = data.loc[2010].groupby('region')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# find the outliers for each category
def outliers(group):
    cat = group.name
    return group[(group.child_mortality > upper.loc[cat]['child_mortality']) | (group.child_mortality < lower.loc[cat]['child_mortality'])]['child_mortality']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in sorted(list(data['region'].unique())):
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

p_mort_2010 = figure(background_fill_color="#EFE8E2", title="Child mortality by region, 2010", x_range=sorted(list(data['region'].unique())))
p_mort_2010.xaxis.major_label_orientation = np.pi/2

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.child_mortality = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'child_mortality']),upper.child_mortality)]
lower.child_mortality = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'child_mortality']),lower.child_mortality)]

p_mort_2010.y_range.start = 0
p_mort_2010.y_range.end = 400

# stems
p_mort_2010.segment(sorted(list(data['region'].unique())), upper.child_mortality, sorted(list(data['region'].unique())), q3.child_mortality, line_color="black")
p_mort_2010.segment(sorted(list(data['region'].unique())), lower.child_mortality, sorted(list(data['region'].unique())), q1.child_mortality, line_color="black")

# boxes
p_mort_2010.vbar(sorted(list(data['region'].unique())), 0.7, q2.child_mortality, q3.child_mortality, fill_color="#E08E79", line_color="black")
p_mort_2010.vbar(sorted(list(data['region'].unique())), 0.7, q1.child_mortality, q2.child_mortality, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p_mort_2010.rect(sorted(list(data['region'].unique())), lower.child_mortality, 0.2, 0.01, line_color="black")
p_mort_2010.rect(sorted(list(data['region'].unique())), upper.child_mortality, 0.2, 0.01, line_color="black")

# outliers
if not out.empty:
    p_mort_2010.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p_mort_2010.xgrid.grid_line_color = None
p_mort_2010.ygrid.grid_line_color = "white"
p_mort_2010.grid.grid_line_width = 2
p_mort_2010.xaxis.major_label_text_font_size="10pt"

p_mort_2010.xaxis.axis_label = 'region'
p_mort_2010.yaxis.axis_label = 'child mortality'



#LIFE HISTOGRAMS

p_hist = figure(title="Life expectancy, 1970", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[1970]['life'], bins=np.arange(20,90,5))

p_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#3B8686", line_color="black")

p_hist.xaxis.axis_label = 'life expectancy'
p_hist.yaxis.axis_label = 'number of countries'

p_hist.xgrid.grid_line_color = None
p_hist.ygrid.grid_line_color = "white"
p_hist.grid.grid_line_width = 2



p_hist_2010 = figure(title="Life expectancy, 2010", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[2010]['life'], bins=np.arange(20,90,5))

p_hist_2010.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                 fill_color="#3B8686", line_color="#033649")

p_hist_2010.xaxis.axis_label = 'life expectancy'
p_hist_2010.yaxis.axis_label = 'number of countries'

p_hist_2010.xgrid.grid_line_color = None
p_hist_2010.ygrid.grid_line_color = "white"
p_hist_2010.grid.grid_line_width = 2


#FERTILITY HISTOGRAMS

p_fert_hist = figure(title="Fertility, 1970", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[1970]['fertility'].dropna(), bins=np.arange(0,10,0.5))

p_fert_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#3B8686", line_color="#033649")

p_fert_hist.xaxis.axis_label = 'fertility'
p_fert_hist.yaxis.axis_label = 'number of countries'

p_fert_hist.xgrid.grid_line_color = None
p_fert_hist.ygrid.grid_line_color = "white"
p_fert_hist.grid.grid_line_width = 2



p_fert_hist_2010 = figure(title="Fertility, 2010", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[2010]['fertility'].dropna(), bins=np.arange(0,10,0.5))

p_fert_hist_2010.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                 fill_color="#3B8686", line_color="#033649")

p_fert_hist_2010.xaxis.axis_label = 'fertility'
p_fert_hist_2010.yaxis.axis_label = 'number of countries'

p_fert_hist_2010.xgrid.grid_line_color = None
p_fert_hist_2010.ygrid.grid_line_color = "white"
p_fert_hist_2010.grid.grid_line_width = 2

#GDP HISTOGRAMS


p_gdp_hist = figure(title="GDP per capita, 1970", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[1970]['gdp'].dropna(), bins=np.arange(0,160000,5000))

p_gdp_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#3B8686", line_color="#033649")

p_gdp_hist.xaxis.axis_label = 'gdp per capita'
p_gdp_hist.yaxis.axis_label = 'number of countries'


p_gdp_hist.xgrid.grid_line_color = None
p_gdp_hist.ygrid.grid_line_color = "white"
p_gdp_hist.grid.grid_line_width = 2


p_gdp_hist_2010 = figure(title="GDP per capita, 2010", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[2010]['gdp'].dropna(), bins=np.arange(0,160000,5000))

p_gdp_hist_2010.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                 fill_color="#3B8686", line_color="#033649")

p_gdp_hist_2010.xaxis.axis_label = 'gdp per capita'
p_gdp_hist_2010.yaxis.axis_label = 'number of countries'

p_gdp_hist_2010.xgrid.grid_line_color = None
p_gdp_hist_2010.ygrid.grid_line_color = "white"
p_gdp_hist_2010.grid.grid_line_width = 2

#CHILD MORTALITY HISTOGRAMS


p_mort_hist = figure(title="Child mortality, 1970", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[1970]['child_mortality'].dropna(), bins=np.arange(0,500,25))

p_mort_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#3B8686", line_color="#033649")

p_mort_hist.xaxis.axis_label = 'child mortality'
p_mort_hist.yaxis.axis_label = 'number of countries'

p_mort_hist.xgrid.grid_line_color = None
p_mort_hist.ygrid.grid_line_color = "white"
p_mort_hist.grid.grid_line_width = 2

p_mort_hist_2010 = figure(title="Child mortality, 2010", background_fill_color="#EFE8E2")

hist, edges = np.histogram(data.loc[2010]['child_mortality'].dropna(), bins=np.arange(0,500,25))

p_mort_hist_2010.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                 fill_color="#3B8686", line_color="#033649")

p_mort_hist_2010.xaxis.axis_label = 'child mortality'
p_mort_hist_2010.yaxis.axis_label = 'number of countries'

p_mort_hist_2010.xgrid.grid_line_color = None
p_mort_hist_2010.ygrid.grid_line_color = "white"
p_mort_hist_2010.grid.grid_line_width = 2

#LINEAR REGRESSIONS

#slope_US, intercept_US = np.polyfit(data_US['Year'].values,data_US['life'].values,1)
#slope_Haiti, intercept_Haiti = np.polyfit(data_Haiti['Year'].values,data_Haiti['life'].values,1)
#slope_China, intercept_China = np.polyfit(data_China['Year'].values,data_China['life'].values,1)

#p_life_lin_reg = figure(title="Life expectancy by country", plot_width=700, plot_height=400)


#p_life_lin_reg.circle(x = data_US['Year'], y = data_US['life'], legend='US', color = Spectral6[0])
#p_life_lin_reg.circle(x = data_Haiti['Year'], y = data_Haiti['life'], legend='Haiti', color = Spectral6[1])
#p_life_lin_reg.circle(x = data_China['Year'], y = data_China['life'], legend='China', color = Spectral6[2])

#p_life_lin_reg.line(x=[1964, 2025], y=[1964 * slope_US + intercept_US, 2025 * slope_US + intercept_US], color = Spectral6[0], legend='US')
#p_life_lin_reg.line(x=[1964,2025], y=[1964 * slope_Haiti + intercept_Haiti, 2025 * slope_Haiti + intercept_Haiti], color = Spectral6[1], legend='Haiti')
#p_life_lin_reg.line(x=[1964,2025], y=[1964 * slope_China + intercept_China, 2025 * slope_China + intercept_China], color = Spectral6[2], legend='China')

#p_life_lin_reg.legend.location = "bottom_right"
#p_life_lin_reg.legend.click_policy="hide"




#REGRESSIONS TEXT INPUT

# Make the ColumnDataSource
source_3 = ColumnDataSource(data={
                          'x'       : data[data['Country'] == 'United States'].reset_index()['Year'],
                          'y'       : data[data['Country'] == 'United States'].reset_index()['life']
                          #'country'      : data.loc[1970].Country,
                          #'region'      : data.loc[1970].region
                          })

# Save the minimum and maximum values of the fertility column
xmin, xmax = 1962, 2015

# Save the minimum and maximum values of the life expectancy column
ymin, ymax = min(data.life), max(data.life)

# Create the figure
p_life_lin_reg = figure(title='Gapminder data for United States', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Set the x-axis label
p_life_lin_reg.xaxis.axis_label ='year'

# Set the y-axis label
p_life_lin_reg.yaxis.axis_label = 'life'

# Make a slider object
textbox = TextInput(value="United States", title="Country:")

#textbox_2 = TextInput(value="China", title="Country 2:")

# Define the callback function
def my_text_input_handler(attr, old, new):
    
    ctry_raw = textbox.value
    ctry = ctry_raw.title()
#   ctry_2 = textbox_2.value
    #x = x_select.value
    y = y_select_2.value
    
    # Label axes of plot
    #plot.xaxis.axis_label = x
    p_life_lin_reg.yaxis.axis_label = y
    
    new_data = {
        'x'       : data[data['Country'] == ctry].reset_index()['Year'],
        'y'       : data[data['Country'] == ctry].reset_index()[y],
#       'z'       : data[data['Country'] == ctry_2].reset_index()[y]
    }
    source_3.data = new_data

    # Set the range of all axes
    #plot.x_range.start = min(data[x])
    #plot.x_range.end = max(data[x])
    p_life_lin_reg.y_range.start = min(data[y])
    p_life_lin_reg.y_range.end = max(data[y])
    
    # Add title to figure
    p_life_lin_reg.title.text = 'Gapminder data for %s' % ctry


# Add the color mapper to the circle glyph
p_life_lin_reg.circle(x='x', y='y', fill_alpha=0.8, source=source_3)

#p_life_lin_reg.circle(x='x', y='z', fill_alpha=0.8, source=source_3, color = 'red')


#p_life_lin_reg.line(x='x', y=[z * np.polyfit('x','y',1)[0] + np.polyfit('x','y',1)[1] for z in 'x'], source=source_3)

textbox.on_change("value", my_text_input_handler)

#textbox_2.on_change("value", my_text_input_handler)

# Create a dropdown Select widget for the y data
y_select_2 = Select(
                  options=['fertility', 'life', 'child_mortality', 'gdp'],
                  value='life',
                  title='y-axis data'
                  )

# Attach the update_plot callback to the 'value' property of y_select
y_select_2.on_change('value', my_text_input_handler)

# Create a HoverTool
hover = HoverTool(tooltips = [('year', '@x'),('y-value', '@y')])

# Add the HoverTool to the plot
p_life_lin_reg.add_tools(hover)

# Set the legend.location attribute of the plot
# if y_select.value == 'life' and x_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'
# elif y_select.value == 'life' and x_select.value == 'gdp':
#     plot.legend.location = 'bottom_right'
# elif y_select.value == 'life' and x_select.value == 'child_mortality':
#     plot.legend.location = 'top_right'
# elif y_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'
# elif y_select.value == 'child_mortality' and x_select.value == 'fertility':
#     plot.legend.location = 'bottom_left'

#plot.legend.location = 'bottom_left'

#plot.legend.click_policy="hide"




#LAYOUT



tab1 = Panel(child=row(widgetbox(slider,x_select,y_select,button), plot), title='Interactive Scatter')

tab2 = Panel(child=row(widgetbox(textbox,y_select_2),p_life_lin_reg), title='By Country')

tab3 = Panel(child = gridplot(p,p_2010,p_hist,p_hist_2010, ncols=2), title='Life Expectancy')

tab4 = Panel(child=gridplot(p_fert,p_fert_2010,p_fert_hist,p_fert_hist_2010, ncols=2), title='Fertility')

tab5 = Panel(child=gridplot(p_gdp,p_gdp_2010,p_gdp_hist,p_gdp_hist_2010,ncols=2), title='GDP Per Capita')

tab6 = Panel(child=gridplot(p_mort,p_mort_2010,p_mort_hist,p_mort_hist_2010, ncols=2), title='Child Mortality')


layout = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])


curdoc().add_root(layout)
#output_notebook()
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


