# print data
# salary = []
# stage = [u'初创型(不需要融资)', u'初创型(天使轮)', u'初创型(未融资)', u'成长型(A轮)', u'成长型(B轮)', u'成长型(不需要融资)', u'成熟型(C轮)', u'成熟型(D轮及以上)', u'成熟型(不需要融资)',u'上市公司']
# for i in [1,3,5,10]:
#     salary = []
#     for j in stage:
#         get_stage_sal_sql = 'select avg(aver_salary) from lagou_data_job where finance_stage = "%s" and years = "%d"'%(j, i)
#         df = pd.read_sql(get_stage_sal_sql, con=mysql_cn)
#         salary.append(int(math.ceil(df['avg(aver_salary)'].values.tolist()[0])))
#     print salary
# citys = ['北京', '上海', '深圳', '杭州', '广州', '成都', '南京', '武汉', '西安', '长沙']

# for i in [1,3,5,10]:
#     salary = []
#     for city in citys:
#         city_sal_sql = 'select avg(aver_salary) from lagou_data_job where city = "%s" and years = "%d"'%(city, i)
#         df = pd.read_sql(city_sal_sql, con=mysql_cn)
#         salary.append(int(math.ceil(df['avg(aver_salary)'].values.tolist()[0])))
#     print salary