# citys = ['北京', '上海', '深圳', '杭州', '广州', '成都', '南京', '武汉', '西安', '长沙']

# for i in [1,3,5,10]:
#     salary = []
#     for city in citys:
#         city_sal_sql = 'select avg(aver_salary) from lagou_lan where city = "%s" and years = "%d"'%(city, i)
#         df = pd.read_sql(city_sal_sql, con=mysql_cn)
#         salary.append(int(math.ceil(df['avg(aver_salary)'].values.tolist()[0])))
#     print salary

# salary = []
# for i in [1,3,5,10]:
#     year_by_salary_sql = 'select aver_salary,count(*) as count from lagou_lan where lan = "C++" and years = "%d" and aver_salary > 50'%(i)
#     df = pd.read_sql(year_by_salary_sql, con=mysql_cn)
#     sal_init = df['count'].values.tolist()[0]
#     sal = int(math.ceil(sal_init)) if sal_init != None else 0
#     salary.append(sal)    
# print salary