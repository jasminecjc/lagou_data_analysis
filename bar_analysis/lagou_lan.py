# -*- coding: utf-8 -*-

from os.path import dirname, join
import numpy as np
import re
import pandas as pd
import MySQLdb
import pprint
import math

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

lan_options = ['All', u'数据挖掘',u'数据可视化',u'数据分析', u'大数据工程师', u'数据架构师']
#lan_options = ['All', 'Javascript','Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']
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

lan = Select(title=u"职位名称", value=u"All", options=lan_options)

 # use create_time
#city = Select(title=u"城市", value=u"All", options=city_options)
# workYear = Select(title=u"工作经验", value=u"All", options=year_options.keys())
# education = Select(title=u"学历要求", value=u"All", options=education_options)
# field = Select(title=u"所在行业", value=u"All", options=field_options)
# output_file("./test.html")
# show(city)

axis_map = {
    u"职位所在城市": "city",
    u"职位所在行业": "fields",
    u"职位所在公司融资阶段": "finance_stage",
    u"职位要求学历": "education",
    u'相应年限工资平均水平': 'aver_salary'
}
x_axis = Select(title=u"分析纬度",
                options=sorted(axis_map.keys()),
                value=u"职位所在行业") 
source = ColumnDataSource(data=dict(x=[], y=[]))
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
get_fields_sql = 'select fields from lagou_data_job'
fields = pd.read_sql(get_fields_sql, con=mysql_cn)
field_list = get_field_list(fields['fields'].values.tolist())
field_count = []
for field in field_list:
    get_field_sql = "select fields, count(*) as count from lagou_data_job where fields like '%"+ field +"%' and job_name = '数据分析' group by fields"
    field_option = pd.read_sql(get_field_sql, con=mysql_cn)
    field_value = sum(field_option['count'].values.tolist())
    field_count.append(field_value)
data = {}
data['fields'] = field_list
data['count'] = field_count
# salary = []
# for i in [1,3,5,10]:
#     year_by_salary_sql = 'select avg(aver_salary) from lagou_lan where lan = "Java" and years = "%d" '%(i)
#     df = pd.read_sql(year_by_salary_sql, con=mysql_cn)
#     sal_init = df['avg(aver_salary)'].values.tolist()[0]
#     sal = math.ceil(sal_init) if sal_init != None else 0
#     salary.append(sal)
# data = {}
# data['sal'] = salary
# data['x'] = [u'1-3年', u'3-5年', u'5-10年', u'10年以上']
# get_city_sql = 'select city,count(*) as count from lagou_data_job where job_name = "数据挖掘" group by city order by count desc limit 0,15'
# df = pd.read_sql(get_city_sql, con=mysql_cn)
# data = {}
# data['city'] = df['city'].values.tolist()
# data['count'] = df['count'].values.tolist()
p = Bar(data, values='count', label='fields', agg='mean',
       title=u"职位所在行业", legend='top_right', width=600)
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

controls = [lan, x_axis]
for control in controls:
    control.on_change('value', update)
update(None, None, None) 
sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
curdoc().add_root(HBox(inputs, p, width=1100))
