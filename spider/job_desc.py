job_dic = {
    '数据可视化': 'data_visualize',
    '数据挖掘': 'data_mining',
    '数据分析': 'data_analysis',
    '大数据工程师': 'data_dev',
    '数据架构师': 'data_arc'
}

def job_desc():
    thread = []
    path = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    keys = job_dic.keys()
    #多线程爬取，每个岗位一个线程
    try:
        for job_title in keys:    
            t = threading.Thread(target=job_crawler,
                              args=(path, job_dic, job_title))
            thread.append(t)
        for i in range(len(keys)):
            thread[i].start()
        for i in range(len(keys)):
            thread[i].join()
    except Exception, e:
        print 'except: 7'
        print e   

def job_crawler(path, job_dic, job_title):
    payload = {'first': 'false', 'pn': '2', 'kd': job_title}
    res = partial(valid_proxy, path, 'post', 0)(payload)
    positions = res[0].json()['content']
    proxies = res[1]
    #获取页码数，按照页码进行抓取
    pages = int(math.ceil(positions['positionResult']['totalCount'] / float(positions['pageSize'])))
    #新建txt文本，如果已经存在进行重写覆盖
    fw = open('%s.txt' % (job_dic[job_title]), 'wt')
    for page in range(1, pages + 1):
        #这里因为拉勾的限制，每用一个ip连续爬取60页就会被封，所以每50个更换一次ip
        if page % 50 == 0:
            proxies = partial(valid_proxy, path, 'post', 0)(payload)[1]
        payload['pn'] = str(page)
        try:  
            jobs = session.post(path, headers = headers, proxies = proxies, data = payload, timeout = 5).json()['content']['hrInfoMap']
            code = 200 if len(jobs) != 0 else 0
        except Exception, e:
            print 'except: 4'
        
        for job in jobs.keys():
            job_path = 'https://www.lagou.com/jobs/%s.html' % (job)
            code = 0
            #循环抓取直到抓取成功
            while code != 200:
                try:  
                    job_detail = session.get(job_path, headers = headers, proxies = proxies, timeout = 5)
                    code = job_detail.status_code
                    #如果出现ip被封的html页面也要更换ip继续
                    notfound = 0 if BeautifulSoup(job_detail.content, "lxml").select('div.i_error') else 1
                    code = notfound and job_detail.status_code
                except Exception, e:
                    print 'except: 5'
                    proxies = {"https": "https://{}".format(get_proxy())}
                try: 
                    #用bs4解析页面存入文档中
                    soup = BeautifulSoup(job_detail.content, "lxml")
                    job_description = soup.select('.job_bt div')
                    job_description = str(job_description[0])
                    rule = re.compile(r'<[^>]+>') 
                    result = rule.sub('', job_description)
                    fw.write(result)
                except Exception, e:
                    print 'except: 6'
    fw.close()

job_desc()