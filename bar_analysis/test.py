
# -*- coding: utf-8 -*-

import re
import pandas as pd
import MySQLdb
import math

from bokeh.charts import Bar
from zhon.hanzi import punctuation
from bokeh.layouts import row
from bokeh.models.widgets import Select
from bokeh.io import curdoc

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

lan_options = ['Javascript','Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']

lan = Select(title=u"编程语言", value=u"All", options=lan_options)

axis_map = {
    u"职位所在城市": "city",
    u"职位所在行业": "fields",
    u"职位所在融资阶段": "finance_stage",
    u"职位要求学历": "education",
    u"相应年限工资平均水平": 'aver_salary'
}

x_axis = Select(title=u"分析纬度",
                options=sorted(axis_map.keys()),
                value=u"职位所在城市") 
get_city_sql = 'select city,count(*) as count from lagou_lan group by city order by count desc limit 0,15'
df = pd.read_sql(get_city_sql, con=mysql_cn)
data = {}
data['city'] = df['city'].values.tolist()
data['count'] = df['count'].values.tolist()
p = Bar(data, values='count', label='city', agg='mean',
        title=u"按城市维度分析", legend='top_right', width=600)

    
def make_bar():
    lan_val = lan.value
    x_name = axis_map[x_axis.value]
    get_level_sql = 'select %s,count(*) as count from lagou_lan where lan="%s" group by %s order by count desc limit 0,15'%(x_name, lan_val, x_name)
    if(lan_val == 'All'):
        get_level_sql = 'select %s,count(*) as count from lagou_lan group by %s order by count desc limit 0,15'%(x_name, x_name)

    options = pd.read_sql(get_level_sql, con=mysql_cn)
    x_options = options[x_name].values.tolist()
    if(x_name == 'aver_salary'):
        salary = []
        get_year_sql = 'select years, count(*) from lagou_lan group by years'
        year_options = pd.read_sql(get_year_sql, con = mysql_cn)
        years = year_options['years'].values.tolist()
        for i in years:
            year_by_salary_sql = 'select avg(aver_salary) from lagou_lan where lan = "%s" and years = "%d" '%(lan, int(i))
            df = pd.read_sql(year_by_salary_sql, con=mysql_cn)
            sal_init = df['avg(aver_salary)'].values.tolist()[0]
            sal = math.ceil(sal_init) if sal_init != None else 0
            salary.append(sal)
        data[x_axis.value] = [u'1-3年', u'3-5年', u'5-10年', u'10年以上']
        data['count'] = salary
        print data
    if(x_name == 'fields'):
        field_list = get_field_list(x_options)
        field_count = []
        for field in field_list:
            get_field_sql = 'select fields, count(*) as count from lagou_lan where fields like "%' + '%s' + '"%'
            field_option = pd.read_sql(get_field_sql, con=mysql_cn)
            print field_option
            field_count.append(field_option.values.tolist()[0])
        data = {}
        data[x_axis.value] = field_list
        data['count'] = field_count
        print data
    else:
        y_values = options['count'].values.tolist()
        data = {}
        data[x_name] = x_options
        data['count'] = y_values
    print data
    p = Bar(data, values='count', label=x_name, agg='mean',
          title=u"按%s维度分析"%(x_axis.value), legend='top_right', width=600)
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = u'数量'
    return p


def update(attr, old, new):
    r1.children[2] = make_bar()
#r1 = row(lan, x_axis, make_bar())
controls = [lan, x_axis]
for control in controls:
    control.on_change('value', update)
#lan.on_change(update)
# x_axis.on_change(update)
r1 = row(lan, x_axis, make_bar())
curdoc().add_root(r1)
# update(None, None, None) 
# sizing_mode = 'fixed'
# inputs = widgetbox(*controls, sizing_mode=sizing_mode)
# curdoc().add_root(HBox(inputs, p, width=1100))


