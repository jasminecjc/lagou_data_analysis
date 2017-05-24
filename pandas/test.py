# -*- coding: utf-8 -*-

from os.path import dirname, join
import numpy as np
import re
import pandas as pd
import MySQLdb
import pprint

from bokeh.plotting import *
from bokeh.charts import Bar, output_file, show
from zhon.hanzi import punctuation
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, HBox, Range1d
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
import codecs
# from bokeh.models import ColumnDataSource, OpenURL, TapTool 
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

mysql_cn= MySQLdb.connect(host="59.110.227.27", user="root", passwd="wjbxlcjc", db="graduate_work", charset="utf8")

def get_field_list(df):
    list = []
    for fields in df:
        if re.search(ur"[%s]+" %punctuation, fields):
            fields = re.sub(ur"[%s]+" %punctuation, ",", fields)
            fields = fields.split(',')
            for field in fields:
                if field not in list:
                    list.append(field)
    return list

getall_sql = 'select * from lagou_lan'
jobs_df = pd.read_sql(getall_sql, con=mysql_cn)


# jobs_df["color"] = np.where(jobs_df["aver_salary"] > 10, "red", "blue")
# jobs_df["alpha"] = np.where(jobs_df["aver_salary"] > 20, 0.9, 0.25)
# jobs_df.fillna(0, inplace=True)

# get_city_sql = 'select city,count(*) as count from lagou_lan group by city order by count desc limit 0,10'
# city_options = pd.read_sql(get_city_sql, con=mysql_cn)
# city_options = city_options['city'].values.tolist()

lan_options = ['All', 'Javascript','Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']

# year_options = {
#     '1-3年': 1,
#     '3-5年': 3,
#     '5-10年': 5,
#     '10年以上': 10
# }

# get_education_sql = 'select education,count(*) as count from lagou_lan group by education'
# education_options = pd.read_sql(get_education_sql, con=mysql_cn)
# education_options = education_options['education'].values.tolist()

# get_field_sql = 'select fields,count(*) as count from lagou_lan group by fields'
# field_values = pd.read_sql(get_field_sql, con=mysql_cn)
# field_values = field_values['fields'].values.tolist()
# field_options = get_field_list(field_values)

lan = Select(title=u"编程语言", value=u"All", options=lan_options)

 # use create_time
#city = Select(title=u"城市", value=u"All", options=city_options)
# workYear = Select(title=u"工作经验", value=u"All", options=year_options.keys())
# education = Select(title=u"学历要求", value=u"All", options=education_options)
# field = Select(title=u"所在行业", value=u"All", options=field_options)
# output_file("./test.html")
# show(city)

axis_map = {
    u"城市": "city",
    u"所在行业": "fields",
    u"融资阶段": "finance_stage",
    u"职位要求学历": "education"
}
x_axis = Select(title=u"分析纬度",
                options=sorted(axis_map.keys()),
                value=u"城市") 
source = ColumnDataSource(data=dict(x=[], y=[]))
# p = figure(plot_height=600,
#            plot_width=800,
#            title="",
#            #toolbar_location=None,
#            tools=[hover,"tap","pan,wheel_zoom,box_zoom,reset,resize,save"],
#            toolbar_location="below",  #http://bokeh.pydata.org/en/latest/docs/user_guide/tools.html
#            )
get_city_sql = 'select city,count(*) as count from lagou_lan group by city order by count desc limit 0,15'
df = pd.read_sql(get_city_sql, con=mysql_cn)
data = {}
data['city'] = df['city'].values.tolist()
data['count'] = df['count'].values.tolist()
#p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tools=["tap","pan,wheel_zoom,box_zoom,reset,resize,save"])
#p = Bar(data, values='count', label='city', agg='mean',
   #       title="count by city", legend='top_right', width=600)
#p.vbar(x=[1,2,3], width=0.5, bottom=0, top=[4,5,6], color="blue")
yr = Range1d(start=0, end=data['count'][0])
p = figure(x_range=data['city'], y_range=yr,plot_height=600, plot_width=700)
p.rect(len(data['city']), [x/2 for x in data['count']] , width=0.5, height=data['count'], color = "blue")
p.xaxis.major_label_orientation = np.pi/4 
def update(attr, old, new):
    lan_val = lan.value
    x_name = axis_map[x_axis.value]
    if(lan_val == 'All'):
        lan_val = 'Javascript'
    
    # use to update plot, not all data
    get_level_sql = 'select %s,count(*) as count from lagou_lan where lan="%s" group by %s limit 0,15'%(x_name, lan_val, x_name)
    options = pd.read_sql(get_level_sql, con=mysql_cn)
    x_options = options[x_name].values.tolist()
    y_values = options['count'].values.tolist()
    data = {}
    data[x_axis.value] = x_options
    data['count'] = y_values
    p = Bar(data, values='count', label=x_axis.value, agg='mean',
          title="c", legend='top_right', width=600)
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = u'数量'
    source.data = dict(x=x_options,
                       y=y_values)


# def update(attr, old, new):
#     r1.children[2] = make_bar()
controls = [lan, x_axis]
for control in controls:
    control.on_change('value', update)
#lan.on_change(update)
# x_axis.on_change(update)
# r1 = row(lan, x_axis, make_bar())
# curdoc().add_root(r1)
update(None, None, None) 
sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
curdoc().add_root(HBox(inputs, p, width=1100))
# def select_jobs():
#     city_val = city.value
#     workYear_val = workYear.value
#     field_val = field.value
#     education_val = education.value
#     lan_val = lan.value
#     assert isinstance(city_val, unicode)
#     selected = jobs_df
#     # selected = jobs_df[
#     #     (jobs_df.salaryAvg >= salaryAvg.value) & (jobs_df.salaryMax >= (
#     #         salaryMax.value)) & (jobs_df.salaryMin >= salaryMin.value)]
#     if (city_val != u"All"):
#         #print type(city_val) #str   | print type(u"北京") <type 'unicode'> | print type("北京") <type 'str'>
#         #selected = selected[selected.city.str.contains("北京") == True] # ok
#         # encode/decode
#         selected = selected[selected.city.str.contains(city_val) == True]
#     if (workYear_val != "All"):
#         selected = selected[selected.workYear.str.contains(
#             workYear_val) == True]
#     if (field_val != "All"):
#         selected = selected[selected.field.str.contains(field_val) ==
#                             True]
#     if (education_val != "All"):
#         selected = selected[selected.education.str.contains(
#             education_val) == True]
#     if (lan_val != "All"):
#         selected = selected[selected.lan.str.contains(
#             lan_val) == True]
#     # make selected < 2000
#     return selected

