# -*- coding: utf-8 -*-

import requests
import MySQLdb
import re
import math
import jieba
import threading
import time
import pprint
from bs4 import BeautifulSoup, NavigableString
from pprint import pprint
from zhon.hanzi import punctuation
from functools import partial

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 


db = MySQLdb.connect(host="59.110.227.27", user="root", passwd="wjbxlcjc", db="graduate_work", charset="utf8")
cursor = db.cursor()


session = requests.session()
    
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
def aver_salary(sal):
    if('-' in sal):
        b = sal.split('-')
        c = (int(b[0][:-1]) + int(b[1][:-1])) / 2
    else:
        c = int(re.split('k|K', sal)[0])
    return c

# lagou
def company_crawler(i, ranges, path, position_path, payload, position_payload, company_sql):
    company_res = []
    for j in range(i - ranges, i + 1):
        payload['pn'] = str(j)
        print j
        if j % 55 == 0:
            proxies = {"https": "https://{}".format(get_proxy())}
        code = 0
        while code != 200:
            try:  
                company_source = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 6).json()
                code = 200 if len(company_source['result']) != 0 else 0
                print i
            except Exception, e:
                print 'except: 2'
                proxies = {"https": "https://{}".format(get_proxy())}
        company_source = partial(valid_proxy, path, 'post', 0)(payload)[0].json()          
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
                tags = soup.select('.con_ul_li')
                company_tags = []
                for tag in tags:
                    company_tags.append(tag.get_text().strip())
                position_payload['companyId'] = company_id
                salary = 0
                for page in range(int(math.ceil(float(company_pos) / 10))):
                    position_payload['pageNo'] = str(page)
                    positions = partial(valid_proxy, position_path, 'post', 0)(position_payload)[0].json()['content']['data']['page']['result']
                    for position in positions:
                        if position['jobNature'] != '全职':
                            continue
                        salary += aver_salary(position['salary'])
                company_salary = 0 if company_pos == 0 else salary / company_pos
                company_res.append((company_name, company_city, company_logo, company_industry, company_stage, company_pos, company_people, company_intro, company_tags, company_salary))          
            except Exception, e:
                print 'except get company data'
                print e
    try:  
        cursor.executemany(company_sql, company_res) 
        db.commit() 
    except Exception, e:
        db.rollback()
        print 'except: sql'
        print e 
# 公司分析
def companys():    
    path = 'https://www.lagou.com/gongsi/0-0-0.json'
    position_path = 'https://www.lagou.com/gongsi/searchPosition.json'
    payload = {'first': 'false', 'pn': '2', 'sortField': '0', 'havemark': '0'}
    position_payload = {'positionFirstType': '全部', 'pageSize': '10'}
    # res = partial(valid_proxy, path, 'post', 0)(payload)
    # source = res[0].json()
    # #proxies = res[1]
    # company_pages = int(math.ceil(int(source['totalCount']) / int(source['pageSize'])))
    #proxies = {"https": "https://{}".format(get_proxy())}
    company_sql = '''insert into lagou_company(name,
                     city, logo_address, industry, finance_stage, position_num, people_num, intro, tags, aver_salary, location)
                     values (%s, %s, %s, %s, %s, %s, %s, %s, "%s", %s, %s)'''
    # try:
    #     thread = []
    #     threadNum = 4 if company_pages % 4 == 0 else 5
    #     ranges = company_pages / 4
    #     for i in range(0, company_pages, company_pages / 4):   
    #         t = threading.Thread(target=company_crawler,
    #                           args=(i, ranges, path, position_path, payload, position_payload, company_sql))
    #         thread.append(t)
    #     for i in range(0, threadNum):
    #         thread[i].start()
    #     for i in range(0, threadNum):
    #         thread[i].join()
    # except Exception, e:
    #     print 'except: 7'
    #     print e  
    company_res = []
    for i in range(1, 5000):
        payload['pn'] = str(i) 
        proxies = {"https": "https://{}".format(get_proxy())}
        code = 0
        while code != 200:
            try:  
                a = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 6)
                print a 
                print a.json()
                company_source = a.json()           
                code = 200 if len(company_source['result']) else 0
            except Exception, e:
                print 'except: 2'
                print e
                proxies = {"https": "https://{}".format(get_proxy())}
                time.sleep(0.5)
        print i         
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
                    #time.sleep(0.1)
                    for position in positions:
                        if position['jobNature'] != '全职':
                            continue
                        salary += aver_salary(position['salary'])
                company_salary = 0 if company_pos == 0 else salary / company_pos
                company_res.append((company_name, company_city, company_logo, company_industry, company_stage, company_pos, company_people, company_intro, company_tags, company_salary, company_location))          
                print len(company_res)
            except Exception, e:
                print 'except get company data'
                print e
        if i % 100 == 0 or i == 5000:
            try:  
                cursor.executemany(company_sql, company_res) 
                print 'sql'
                db.commit() 
                company_res = []
            except Exception, e:
                db.rollback()
                print 'except: sql'
                print e 
    
    
    #soup = BeautifulSoup(source.content)
    #print soup   
    # company_total = soup.select('div.details')[0]
    # count = 0
    # company_value = []
    # payload = {'first': 'false', 'pn': '2', 'sortField': '0', 'havemark': '0'}
    # companys_sql = '''insert into lagou_companys(level,
    #                   tag, totalCount)
    #                   values (%s, %s, %s)'''
    # #公司分析
    # for index, child in enumerate(company_total.children):
    #     if isinstance(child, NavigableString):
    #         count += 1
    #         continue
    #     child_class = child['class'][-1]
    #     child_tags = soup.select('.%s a' % (child_class)) if child_class == 'financeStage' else company_total.select('.%s .hot a' % (child_class))
    #     for i in child_tags[1::]:
    #         data_id = i['data-id']
    #         init_index = ['0', '0', '0']
    #         init_index[index - count] = str(data_id)
    #         index_param = '-'.join(init_index)
    #         industry_path = '%s/%s.json' % (path, index_param)
    #         companys = partial(valid_proxy, industry_path, 'post', 0)(payload)[0].json()
    #         company_value.append((i.get_text().strip(), child_class, int(companys['totalCount'])))
    
    # try:                     
    #     cursor.executemany(companys_sql, company_value)    
    #     db.commit() 
    # except Exception, e:
    #     db.rollback()
    #     print 'except: sql'
    #     print e     
    # #C轮以及以上公司行业
    # stage_index = '0-5,6,7-0'
    # stage_path = '%s/%s.json' % (path, stage_index)
    # res = partial(valid_proxy, stage_path, 'post', 0)(payload)
    # stage_companys = res[0].json()
    # proxies = res[1]
    # stage_count = int(stage_companys['totalCount'])
    # stage_pages = int(math.ceil(stage_count / int(stage_companys['pageSize'])))
    # fields_dic = dict()
    # fw = open('company_feature.txt', 'w+')
    # for i in range(2, stage_pages):
    #     #临界值60
    #     payload['pn'] = str(i)
    #     if i % 50 == 0:
    #         proxies = {"https": "https://{}".format(get_proxy())}
    #     code = 0
    #     while code != 200:
    #         try:  
    #             pn_companys = session.post(stage_path, headers = headers, proxies = proxies, data = payload, timeout = 20).json()
    #             code = 200 if len(pn_companys['result']) != 0 else 0
    #             print i
    #         except Exception, e:
    #             print 'except: 2'
    #             proxies = {"https": "https://{}".format(get_proxy())}
    #     print pn_companys['pageNo']
    #     for details in pn_companys['result']:
    #         feature = details['companyFeatures']
    #         fw.write(feature)
    #         fields = details['industryField'].strip()
    #         if re.search(ur"[%s]+" %punctuation, fields):
    #             fields = re.sub(ur"[%s]+" %punctuation, ",", fields)
    #         fields = fields.split(',')
    #         for field in fields:
    #             if field.strip() not in fields_dic:
    #                 fields_dic[field.strip()] = 1
    #             fields_dic[field.strip()] += 1
    # fw.close()
    # fields_value = []
    # for (key, val) in fields_dic.items():
    #     fields_value.append((key, 'field', val))
    # try:  
    #     cursor.executemany(companys_sql, fields_value) 
    #     db.commit() 
    # except Exception, e:
    #     db.rollback()
    #     print 'except: sql'
    #     print e
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
            if page % 50 == 0:
                proxies = partial(valid_proxy, path, 'post', 0)(payload)[1]
            payload['pn'] = str(page)
            code = 0
            while code != 200: 
                try:  
                    pn_job = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 5).json()['content']['positionResult']['result']
                    print 'page: %s' % (page)
                    code = 200
                except Exception, e:
                    print 'except: 3'
                    proxies = {"https": "https://{}".format(get_proxy())}
            for list in pn_job:
                if list['jobNature'] != '全职' or workyear_dic.has_key(list['workYear']) == False:
                    continue
                years = workyear_dic[list['workYear']] or 'unknown'
                city = list['city'] or 'unknown'
                salary = aver_salary(list['salary']) or 0
                stage = list['financeStage'] or 'unknown'
                education = list['education'] or 'unknown'
                fields = list['industryField'] or 'unknown'
                job_value.append((job, city, salary, years, stage, education, fields))
            if page % 50 == 0 or page == pages:        
                try:  
                    cursor.executemany(job_sql, job_value)
                    print 'sql'
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

#program_lan()
companys()



def data_job():
    path = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false' 
    data_job_sql = '''insert into lagou_data_job(job_name,
                 city, aver_salary, years, finance_stage, education, fields)
                 values (%s, %s, %s, %s, %s, %s, %s)'''
    job_count(job_dic.keys(), path, data_job_sql)

#data_job()
