import pandas as pd
import numpy as np
import MySQLdb
import re
from zhon.hanzi import punctuation
from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.charts.utils import df_from_json

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

mysql_cn= MySQLdb.connect(host="59.110.227.27", user="root", passwd="wjbxlcjc", db="graduate_work", charset="utf8")

class lagou_lan_analysis:
	def __init__(self, lan_list, city_sql):
		self.lan_list = lan_list
		self.city_sql = city_sql
	
	def get_by_city(self):
		df = pd.read_sql(self.city_sql, con=mysql_cn)
		df = df.sort_values(['count'], ascending=[False])
		data = {}
		data['city'] = df['city'].values.tolist()
		data['count'] = df['count'].values.tolist()
		bar = Bar(data, values='count', label='city', agg='mean',
          title="count by city", legend='top_right', width=600)
		output_file('./test.html')
		show(bar)

	def get_by_lan_stage(self):
		stage_sql = 'select finance_stage,count(*) as count from lagou_lan where lan = "PHP" group by finance_stage'
		df = pd.read_sql(stage_sql, con=mysql_cn)
		data = {}
		data['finance_stage'] = df['finance_stage'].values.tolist()
		data['count'] = df['count'].values.tolist()
		bar = Bar(data, values='count', label='finance_stage', agg='mean',
      title="count by finance_stage", color='blue', legend='top_right', width=600)
		show(bar)
		output_file('./test.html')
	def get_by_year_salary(self):
		for lan in self.lan_list:
			for i in [1,3,5,10]:
				year_by_salary_sql = 'select avg(aver_salary) from lagou_lan where lan = "%s" and years = "%d" '%(lan, i)
				df = pd.read_sql(year_by_salary_sql, con=mysql_cn) 
				print df

	def get_by_fields(self):
		field_sql = 'select fields,count(*) as count from lagou_lan where lan = "PHP" group by fields'
		field_sql = 'select  fields from lagou_lan where lan = "PHP" limit 1'
		df = pd.read_sql(field_sql, con=mysql_cn)
		print df['fields'].values.tolist()

if __name__ == '__main__':
	lan_list = ['Javascript','Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']
	city_sql = 'select city,count(*) as count from lagou_lan group by city order by count desc limit 0,10'
	get_lan_analysis = lagou_lan_analysis(lan_list, city_sql)
	get_lan_analysis.get_by_city()
	# get_lan_analysis.get_by_lan_stage()
	# get_lan_analysis.get_by_year_salary()
	# get_lan_analysis.get_by_fields()
	
	