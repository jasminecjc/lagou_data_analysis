
# -*- coding: utf-8 -*-

import re
import pandas as pd
import MySQLdb
import math

#引入bokeh依赖
from bokeh.charts import Bar
from bokeh.plotting import figure, output_file, show
from zhon.hanzi import punctuation
from bokeh.layouts import row, column
from bokeh.models.widgets import Select
from bokeh.io import curdoc

#设置编码
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

mysql_cn= MySQLdb.connect(host="59.110.227.27", user="root", passwd="wjbxlcjc", db="graduate_work", charset="utf8")

#把移动互联网，数据服务这种形式的切割成单独的词
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

get_fields_sql = 'select fields from lagou_lan'
fields = pd.read_sql(get_fields_sql, con=mysql_cn)
field_list = get_field_list(fields['fields'].values.tolist())

lan_options = ['All', 'Javascript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']

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

get_city_sql = 'select city,count(*) as count from lagou_lan group by city order by count desc limit 0, 15'
df = pd.read_sql(get_city_sql, con=mysql_cn)
data = {}
data['city'] = df['city'].values.tolist()
data['count'] = df['count'].values.tolist()

p = Bar(data, values='count', label='city', agg='mean',
        title=u"按城市维度分析", legend='top_right', width=600)

# 更新图表
def make_bar():
    lan_val = lan.value
    x_name = axis_map[x_axis.value]
    get_level_sql = 'select %s,count(*) as count from lagou_lan where lan="%s" group by %s order by count desc limit 0,15'%(x_name, lan_val, x_name)
    if(lan_val == 'All'):
        get_level_sql = 'select %s,count(*) as count from lagou_lan group by %s order by count desc limit 0,15'%(x_name, x_name)

    options = pd.read_sql(get_level_sql, con=mysql_cn)
    x_options = options[x_name].values.tolist()
    data = {}
    #取出薪水平均值
    if(x_name == 'aver_salary'):
        salary = []
        for i in [1,3,5,10]:
            year_by_salary_sql = 'select avg(aver_salary) from lagou_lan where lan = "%s" and years = "%d"'%(lan_val, i)
            if(lan_val == 'All'):
                year_by_salary_sql = 'select avg(aver_salary) from lagou_lan where years = "%d"'%(i)
            df = pd.read_sql(year_by_salary_sql, con=mysql_cn)
            sal_init = df['avg(aver_salary)'].values.tolist()[0]
            sal = math.ceil(sal_init) if sal_init != None else 0
            salary.append(sal)    
        data['count'] = salary
        data[x_name] = [u'1-3年', u'3-5年', u'5-10年', u'10年以上']
    elif(x_name == 'fields'):
        field_count = []
        for field in field_list:
            get_field_sql = "select fields, count(*) as count from lagou_lan where fields like '%"+ field +"%' and lan = '%s' group by fields"%(lan_val)
            field_option = pd.read_sql(get_field_sql, con=mysql_cn)
            field_value = sum(field_option['count'].values.tolist())
            field_count.append(field_value)
        data[x_name] = field_list
        data['count'] = field_count
    else:
        y_values = options['count'].values.tolist()
        data = {}
        data[x_name] = x_options
        data['count'] = y_values
    p = Bar(data, values='count', label=x_name, agg='mean',
          title=u"按%s维度分析"%(x_axis.value), legend='top_right', width=600)
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = u'数量'
    return p

def update(attr, old, new):
    r1.children[1] = make_bar()

controls = [lan, x_axis]
for control in controls:
    control.on_change('value', update)
col = column(lan, x_axis)
r1 = row(col, make_bar())
curdoc().add_root(r1)


