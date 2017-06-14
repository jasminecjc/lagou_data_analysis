# -*- coding: utf-8 -*-
#引入依赖包
import requests
import MySQLdb
import re
import math
from bs4 import BeautifulSoup, NavigableString
#zhon是用来处理中文标点符号的包
from zhon.hanzi import punctuation
from functools import partial

#设置utf-8编码
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

#连接数据库
db = MySQLdb.connect(host="yourhost", user="root", passwd="yourpwd", db="yourdb", charset="utf8")
cursor = db.cursor()

session = requests.session()
    
#设置http头，应对反爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Cookie': 'LGUID=20160223140504-620c0982-d9f3-11e5-8b4c-525400f775ce; tencentSig=6558885888; user_trace_token=20170228174718-e5fb608afce74f799b7776b1047078c6; fromsite=www.google.co.jp; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=903d052305ac48cd89da8777f732ed0d; JSESSIONID=937760D5DB1DE2F81DA0B920D449CE9F; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgqHLbZOanuNKiqmYhHa76U6q7FKEDxhDErLFpCoECiO%26wd%3D%26eqid%3D8df355dc0004eb9b0000000258e7a7eb; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_company; _ga=GA1.2.507913091.1456207502; LGSID=20170407225346-009efbed-1ba2-11e7-9d24-5254005c3644; LGRID=20170407225432-1bd38d70-1ba2-11e7-9d24-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1491466928,1491556280,1491576814,1491576825; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1491576870'
}

def get_proxy():
    return requests.get("http://127.0.0.1:5000/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(proxy))

def valid_proxy(path, method, code = 0, *payload):
    while code != 200:
        try:  
            proxies = {"https": "https://{}".format(get_proxy())}
            if method == 'get':     
                source = session.get(path, headers = headers, proxies = proxies, timeout = 5)
            else:
                source = session.post(path, headers = headers, proxies = proxies, data = payload[0], timeout = 5) 
            try:
                notfound = len(source.json()['result'])
            except:
                notfound = 0 if BeautifulSoup(source.content,"lxml").select('div.i_error') else 1
            code = notfound and source.status_code
        except Exception, e:
            print 'except: 1'
            print e
    return [source, proxies]
#从10k-20k这样的格式获取到平均工资
def aver_salary(sal):
    if('-' in sal):
        b = sal.split('-')
        c = (int(b[0][:-1]) + int(b[1][:-1])) / 2
    else:
        c = int(re.split('k|K', sal)[0])
    return c

# 公司分析
# def companys():    
    path = 'https://www.lagou.com/gongsi/0-0-0.json'
    position_path = 'https://www.lagou.com/gongsi/searchPosition.json'
    payload = {'first': 'false', 'pn': '2', 'sortField': '0', 'havemark': '0'}
    position_payload = {'positionFirstType': '全部', 'pageSize': '10'}
    res = partial(valid_proxy, path, 'post', 0)(payload)
    source = res[0].json()
    company_pages = int(math.ceil(int(source['totalCount']) / int(source['pageSize'])))
    company_sql = '''insert into lagou_company(name,
                     city, logo_address, industry, finance_stage, position_num, people_num, intro, tags, aver_salary, location)
                     values (%s, %s, %s, %s, %s, %s, %s, %s, "%s", %s, %s)'''

    company_res = []
    for i in range(1, company_pages + 1):
        payload['pn'] = str(i) 
        code = 0
        while code != 200:
            try:  
                company_source = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 6).json()  
                print company_source      
                code = 200 if len(company_source['result']) else 0
            except Exception, e:
                print 'except: 2'
                print e
        for company in company_source['result']:
            try: 
                company_id = company['companyId']
                company_name = company['companyShortName']
                company_city = company['city']
                company_logo = company['companyLogo']
                company_stage = company['financeStage']
                company_pos = company['positionNum']
                company_industry = company['industryField']
                company_path = 'https://www.lagou.com/gongsi/%s.html' % (company_id)
                company_home = partial(valid_proxy, company_path, 'get', 0)()[0]
                soup = BeautifulSoup(company_home.content, "lxml")
                company_people = soup.select('.number')[0].parent.get_text().strip()
                company_intro = soup.select('.company_content')[0].get_text()
                company_location = soup.select('.mlist_li_desc')[0].get_text()
                tags = soup.select('.con_ul_li')
                company_tags = []
                for tag in tags:
                    company_tags.append(tag.get_text().strip())
                position_payload['companyId'] = company_id
                salary = 0
                for page in range(int(math.ceil(float(company_pos) / 10))):
                    position_payload['pageNo'] = str(page)
                    positions = partial(valid_proxy, position_path, 'post', 0)(position_payload)[0].json()['content']['data']['page']['result']
                    time.sleep(1)
                    for position in positions:
                        if position['jobNature'] != '全职':
                            continue
                        salary += aver_salary(position['salary'])
                company_salary = 0 if company_pos == 0 else salary / company_pos
                company_res.append((company_name, company_city, company_logo, company_industry, company_stage, company_pos, company_people, company_intro, company_tags, company_salary, company_location))          
                #print len(company_res)
            except Exception, e:
                print 'except get company data'
                print e
            try:  
                cursor.executemany(company_sql, company_res) 
                print 'sql'
                db.commit() 
                company_res = []
            except Exception, e:
                db.rollback()
                print 'except: sql'
                print e 
#companys()          

workyear_dic = {
    u'\u0031\u002d\u0033\u5e74': 3,
    u'\u0033\u002d\u0035\u5e74': 5,
    u'\u0035\u002d\u0031\u0030\u5e74': 10,
    u'\u4e0d\u9650': 1
}
job_dic = {
    '数据可视化': 'data_visualize',
    '数据挖掘': 'data_mining',
    '数据分析': 'data_analysis',
    '大数据工程师': 'data_dev',
    '数据架构师': 'data_arc'
}

payload = {'first': 'false', 'pn': '2', 'kd': ''}

def job_count(job_list, path, job_sql):
    job_value = []
    for job in job_list:
        payload['kd'] = job
        res = partial(valid_proxy, path, 'post', 0)(payload)
        positions = res[0].json()['content']
        proxies = res[1]
        pages = int(math.ceil(positions['positionResult']['totalCount'] / positions['pageSize']))
        for page in range(1, pages + 1):
            if page == 1:
                payload['first'] = 'true'
            #这里因为拉勾的限制，每用一个ip连续爬取60页就会被封，所以每50个更换一次ip
            if page % 50 == 0:
                proxies = partial(valid_proxy, path, 'post', 0)(payload)[1]
            payload['pn'] = str(page)
            code = 0
            while code != 200: 
                try:  
                    pn_job = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 5).json()['content']['positionResult']['result']
                    code = 200
                except Exception, e:
                    print 'except: 3'
                    proxies = {"https": "https://{}".format(get_proxy())}
            for list in pn_job:
                #排除实习的信息和工作年限在定义之外的信息
                if list['jobNature'] != '全职' or workyear_dic.has_key(list['workYear']) == False:
                    continue
                years = workyear_dic[list['workYear']] or 'unknown'
                city = list['city'] or 'unknown'
                salary = aver_salary(list['salary']) or 0
                stage = list['financeStage'] or 'unknown'
                education = list['education'] or 'unknown'
                fields = list['industryField'] or 'unknown'
                job_value.append((job, city, salary, years, stage, education, fields))
            #每50页，即750条写入一次数据库，或者等页码到总页码数时写入
            if page % 50 == 0 or page == pages:        
                try:  
                    cursor.executemany(job_sql, job_value)
                    job_value = []
                    db.commit() 
                except Exception, e:
                    db.rollback()
                    print 'except: sql'
                    print e        
def program_lan():
    path = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    lan_list = ['Javascript','Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Scala']
    
    lan_sql = '''insert into lagou_lan(lan,
                 city, aver_salary, years, finance_stage, education, fields)
                 values (%s, %s, %s, %s, %s, %s, %s)'''
    job_count(lan_list, path, lan_sql)



def data_job():
    path = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false' 
    data_job_sql = '''insert into lagou_data_job(job_name,
                 city, aver_salary, years, finance_stage, education, fields)
                 values (%s, %s, %s, %s, %s, %s, %s)'''
    job_count(job_dic.keys(), path, data_job_sql)
    
program_lan()
data_job()
