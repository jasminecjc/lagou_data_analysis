### 功能点

#### 爬取数据

* 所有公司数据，名称简写，城市，行业，职位数量，人数范围，标签，介绍，融资阶段，
  平均工资
* github2016 年度最受欢迎编程语言相应年数薪水，城市，学历要求，公司融资阶段，公
  司行业
* 大数据行业五大岗位相应年数薪水，城市，学历要求，公司融资阶段，公司行业，岗位要
  求

#### 编程语言分析

* 编程语言在不同城市 (top10) 的需求量
* 编程语言在不同行业 (top10) 的需求量
* 编程语言在不同融资阶段的需求量
* 编程语言相应工作年限薪水平均值

#### 大数据岗位分析

* 五个岗位的职位需求关键词词云
* 五个岗位在不同城市 (top10) 的需求量
* 五个岗位在不同行业 (top10) 的需求量
* 五个岗位在不同融资阶段的需求量
* 五个岗位相应工作年限薪水平均值

#### 数据可视化

* Bokeh
* Echarts

### 开发工作

* 编写数据采集所用语言：python
* 针对拉勾网反爬虫的应对措施：
  * 加 http 头伪装成浏览器；
  * 找临界值更换 IP；
  * 限制爬取频率；
  * 设置代理池。
* 使用多线程爬虫：提高效率
* 制作词云：jieba 中文分词，自定义词典，wordcloud 生成图片
* 分析结果可视化：bokeh ， echarts

### 数据岗位分析结果

* 数据岗位不同城市需求增长趋势 2016.02 数据
  ![图片 1.png](file:///Users/chengjiachen/Desktop/ 图片 1.png) 2017.05 数据
  ![2.png](file:///Users/chengjiachen/Desktop/2.png) 可以看到 TOP5 城市依然未变
  ，南京武汉的数据岗位增加明显，数量上而言，总体翻倍

* 数据分析岗位增长趋势 `数据分析相关专业作为新兴行业在近一年来的发展势头迅猛
  ，2016 年 10 月之前的招聘信息十分稀少，但在短短四个月的时间内增长至一千多个
  。(2016.10-2017.1)` 2017.02 数据
  ![3.png](file:///Users/chengjiachen/Desktop/3.png) 2017.05 数据
  ![4.png](file:///Users/chengjiachen/Desktop/4.png)

* 数据岗位工资水平两年内变化 2015 年数据岗位相应工作年限平均工资
  ![5.png](file:///Users/chengjiachen/Desktop/5.png) 2017.05 数据岗位相应工作年
  限平均工资数据 ![6.png](file:///Users/chengjiachen/Desktop/6.png) 可以看出，两
  年内数据岗位的工资明显提高，起薪近乎涨了一倍，各个年限增长趋势也很明显。

* 数据挖掘工资趋势 2015.12 数据
  ![7.png](file:///Users/chengjiachen/Desktop/7.png) 2017.05 数据
  ![8.png](file:///Users/chengjiachen/Desktop/8.png) 总体都比两年前对应年薪高，
  并且高薪比例明显提高

* 数据岗位和普通开发不同年限工资对比普通开发岗位工资水平
  ![9.png](file:///Users/chengjiachen/Desktop/9.png) 数据岗位工资水平
  ![10.png](file:///Users/chengjiachen/Desktop/10.png) 3-5 年和 5-10 年的工资水
  平没有明显增长，也许说明重复的劳动不能代表技术的增长

* 数据岗位和普通开发岗位要求学历对比
  ![13.png](file:///Users/chengjiachen/Desktop/13.png)
  ![14.png](file:///Users/chengjiachen/Desktop/14.png) 可以看出，数据岗位对学历
  的要求较普通开发高，硕士的比例增加，并出现了博士的需求。

* 词云结果实例 数据架构师岗位要求词云
  ![3d295a7d7670bfda.png](file:///Users/chengjiachen/Documents/images/3d295a7d7670bfda.png)
  可以看出对架构师而言，“ 开发 ” 还是最重要的，“ 架构设计 ” 毫无疑问成为关键词，
  另外管理能力也有所要求 数据分析师岗位要求词云
  ![ac31c3db3e0a6ea4.png](file:///Users/chengjiachen/Documents/images/ac31c3db3e0a6ea4.png)
  数据挖掘岗位要求词云
  ![048a518cf0892fea.png](file:///Users/chengjiachen/Documents/images/048a518cf0892fea.png)
  可以看到算法成为了一大关键词，说明数据挖掘对算法的要求还是挺高的，另外 “ 计算
  机 ” 和 “ 数学 ” 成为了需求最多的两个专业，编程语言方面 “SQL”,“ JAVA”,“ R” 都
  有要求。 数据可视化岗位要求词云
  ![e0df5ae5ce432651.png](file:///Users/chengjiachen/Documents/images/e0df5ae5ce432651.png)
  可以看到前端成为了一个关键词，另外可视化相应的工具如 “ECHARTS” 等也出现在词云
  中，交互和开发同时出现，这在其他岗位是没有的，说明可视化还是需要视觉效果
  ### 2016github10 大热门编程语言现状分析
* 职位需求量
  ![de31b8cd3c89e2a4.png](file:///Users/chengjiachen/Documents/images/de31b8cd3c89e2a4.png)
* 所在行业 Python 岗位所在行业
  ![d24d83dcda2e70c5.png](file:///Users/chengjiachen/Documents/images/d24d83dcda2e70c5.png)
  scala 岗位所在公司行业
  ![7672bc81da0f18dc.png](file:///Users/chengjiachen/Documents/images/7672bc81da0f18dc.png)
  可以看出 Python 的应用更广，而 Scala 主要是数据服务行业需要。原因是 Python 除
  了可以用来做 web 开发，在科学计算等方面的表现也很出色。
* 岗位城市分布 ( 示例 java) Java 岗位城市分布
  ![6ef21207a638af5b.png](file:///Users/chengjiachen/Documents/images/6ef21207a638af5b.png)
  可以看出 Java 的总体需求还是北上广深杭比较多，而杭州数量多的可能也许是因为坐落
  在此的阿里巴巴内部使用 Java 较多
* 岗位所在公司融资阶段 ( 示例 PHP)
  ![55fbc6264d4cd53e.png](file:///Users/chengjiachen/Documents/images/55fbc6264d4cd53e.png)
  对 PHP 需求最多的是初创型公司，可能因为 PHP 可以做到快速开发并且在中小规模公司
  比较适用。

### 多维度分析

普通开发不同城市不同工作年限平均工资
![11.png](file:///Users/chengjiachen/Desktop/11.png) 可以看出，北京的整体工资水
平最高，高薪主要集中在北上广深杭，其中，杭州的工资水平也较高，可能因为杭州是阿里
巴巴网易等大型互联网公司总部所在地。

不同融资阶段公司工作年限不同平均工资
![12.png](file:///Users/chengjiachen/Desktop/12.png) 可以看到 1-3 年和 3-5 年工
资差距并不明显，D 轮及以上公司给的工资整体水平都比其他融资阶段高

### 分析结论

* 数据岗位集中在北上广深，需求量呈爆炸式增长。
* 数据岗位算法、学历要求更高，对业务敏锐，薪资更高。
* 门槛高的岗位需求量更少 (Scala), 门槛低应用广 (Python)
* 互联网行业对人才的要求越来越高（算法、数学、业务）
