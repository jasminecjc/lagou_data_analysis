def job_desc():

    thread = []
    path = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    keys = job_dic.keys()
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
    pages = int(math.ceil(positions['positionResult']['totalCount'] / float(positions['pageSize'])))
    fw = open('%s.txt' % (job_dic[job_title]), 'wt')
    for page in range(1, pages + 1):
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
            while code != 200:
                try:  
                    job_detail = session.get(job_path, headers = headers, proxies = proxies, timeout = 5)
                    code = job_detail.status_code
                    notfound = 0 if BeautifulSoup(job_detail.content, "lxml").select('div.i_error') else 1
                    code = notfound and job_detail.status_code
                except Exception, e:
                    print 'except: 5'
                    proxies = {"https": "https://{}".format(get_proxy())}
                try: 
                    soup = BeautifulSoup(job_detail.content, "lxml")
                    job_description = soup.select('.job_bt div')
                    job_description = str(job_description[0])
                    rule = re.compile(r'<[^>]+>') 
                    result = rule.sub('', job_description)
                    fw.write(result)
                except Exception, e:
                    print 'except: 6'
    fw.close()

#job_desc()