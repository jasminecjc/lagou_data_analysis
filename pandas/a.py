from os.path import dirname, join

import pandas as pd

from bokeh.layouts import layout, widgetbox
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select
from bokeh.charts import Bar, output_server
from bokeh.io import curdoc
from bokeh.models import NumeralTickFormatter

# Convert CSV file to Dataframe
data = pd.read_csv('data.csv')
pd.to_numeric(data['price'])

# Get Maximum Price
maxPrice = data['price'].max()

# City Options Drop-down
cityListWithAll = list(set(data['city']))
cityListWithAll.insert(0, 'ALL')
cityListWithAll.sort()

# HTML Template
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=900)

# Create Input controls
min_price = Slider(title="Minimum Price", start=1, end=maxPrice, value=1, step=100000000)
max_price = Slider(title="Maximum Price", start=1, end=maxPrice, value=maxPrice, step=100000000)
city = Select(title="City", value="ALL", options=cityListWithAll)
item_type = Select(title="Item Type", value="ALL", options=open(join(dirname(__file__), 'item_type.txt')).read().split())


# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(values=[], label=[], price=[], city=[]item_type=[]))

# Create Bar Chart
p = Bar(data, values="price", label="city", title="Average Price", agg='mean',
        plot_width=800, tools='hover', legend=None)

# Filtering Functions
def select_filter():
    city_val = city.value
    item_type_val = item_type.value
    offer_type_val = offer_type.value

    selected = data[
        (data.price >= min_price.value) &
        (data.price <= max_price.value)
    ]

    if (city_val != "ALL"):
        selected = selected[selected.city.str.endswith(city_val) == True]
    if (item_type_val != "ALL"):
        selected = selected[selected.item_type.str.contains(item_type_val) == True]
		
    print selected
    return selected

def update():
    df = select_filter()
    values_val = 'price'
    label_val = 'city'

    source.data = dict(
        values = df[values_val],
        label = df[label_val],
        price=df['price'],
        city=df['city'],
        item_type=df['item_type'],
    )


# Controller Listeners
controls = [min_price, max_price, city, item_type]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()

# Output
curdoc().add_root(l)
curdoc().title = "AVG Price"