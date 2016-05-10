# -*- coding:utf-8 -*-

"""Made by Viki Qiu during 2016/5/7-2016/5/11"""

import urllib2 # 使用header
import re # 正则
import time # 延时
import traceback # 错误判断

def get_page_urls(str,a,b):
    """
    获得每一页总页的url
    如: https://book.douban.com/subject/1007305/reviews?score=&amp;start=25
    @str: "https://book.douban.com/subject/1007305/reviews?score=&amp;start="
    @n: 总共的页数
    2016/5/10 23:36 整理完毕
    """
    page_urls=[]
    for i in range(a,b):
        page_urls.append("%s%d" % (str,i*25))
        #print i
    return page_urls

def get_content(url):
    """
    输入一个url字符串，输出对应的html内容
    @url: 要爬的一个链接
    尚未解决：1、多个agent2、cookies设置3、多个ip轮换
    2016/5/10 22:58 整理完毕
    """

    req=urllib2.Request(url)

    req.add_header("user-agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36")
    req.add_header("GET",url)
    req.add_header("host","book.douban.com")

    html=urllib2.urlopen(req)
    content=html.read()
    html.close()

    return content

def get_first_info(html):
    """ 
    获得该总页信息：
    return 标题、链接、姓名、时间 均为字符串，总返回一个tuple
    @html:某个总页url的html内容，由get_content返回
    2016/5/10 23：09 整理完毕
    """
    regex_url=r'href="(.+?)" class="j a_unfolder"'
    pat = re.compile(regex_url)
    regex_title=r'<a title="(.+?)"'
    pat_title=re.compile(regex_title)
    regex_name=r'class=" ">(.+?)</a>'
    pat_name=re.compile(regex_name)
    regex_time=r'<span class="">(.+?)</span> &nbsp; &nbsp;'
    pat_time=re.compile(regex_time)

    comment_url=re.findall(pat,html)
    comment_title=re.findall(pat_title,html)
    comment_name=re.findall(pat_name,html)
    comment_time=re.findall(pat_time,html)

    return comment_title,comment_url,comment_name,comment_time

def get_all_info(urls):
    """
    输入url数组，获得urls中每个url的总页信息，其中每个url为总页url
    @urls:为page_urls获得的数组，每个url为一个总页
    @return：urls,titles,names,stars,times 均为数组
    2016/5/10 23:44 整理完毕
    """
    comment_urls=[]
    titles=[]
    names=[]
    times=[]
    i=0
    for url in urls:
        print(url)
        html=get_content(url)
        info=get_first_info(html)
        comment_urls.extend(info[1])
        titles.extend(info[0])
        names.extend(info[2])
        times.extend(info[3])
        print "page=%d"%i
        i += 1
        # print titles[0],names[0],times[0],comment_urls[0]
    return titles,names,times,comment_urls

def get_sep_info(urls):
    """
    输入一个url数组，获得每一个url的分页信息，其中每个url为分页url
    return stars,respons,goods,totals,comments 均为数组，组成tuple
    2016/5/10 23:57 整理完毕
    """
    print "get_sep_info"
    stars=[];goods=[];totals=[];comments=[];i=0;respons=[]
    for url in urls:
        print url,i
        good="NA";total="NA";comment="NA";star="NA";respon="NA"
        html=get_content(url)
        regex_star=r'<span title="(.+?)">'
        pat_star = re.compile(regex_star)
        regex_judge=r'<em id=(.+?)</em>'
        pat_judge=re.compile(regex_judge)
        regex_comment=r'<span property="v:description" class="">(.+?)<div class="clear"></div></span>'
        pat_comment=re.compile(regex_comment)
        regex_respon=r'<div class="bd">(.)'
        pat_respon=re.compile(regex_respon)

        star=re.findall(pat_star,html)
        if len(star)==0: 
            stars="NA"
        else:
            star=star[0] # 转为字符型，防止ascii乱码
        try: # 防止页面错误跳到主页
            good=re.findall(pat_judge,html)[0].split(">")[1]
        except:
            print "NO PAGE"
            stars.append(star)
            goods.append(good)
            totals.append(total)
            respons.append(respon)
            comments.append(comment)
            continue
        total=re.findall(pat_judge,html)[1].split(">")[1]
        if good=="":good="NA"
        if total=="":total="NA"
        stars.append(star)
        goods.append(good)
        totals.append(total)
        comment=re.findall(pat_comment,html)[0]
        comment=comment.decode('utf-8','ignore').encode('utf-8').strip()
        comments.append(comment)
        respon=str(len(re.findall(pat_respon,html)))
        respons.append(respon)
        i+=1
        if i%5==0:time.sleep(4) # 设置沉睡时间，控制在1min40个页面以内
        # print star[0],respons[0],good[0],total[0],comments[0]
    return stars,respons,goods,totals,comments

def get_info(pattern,a,b):
    """
    输入pattern以及起止页，获得信息并写出
    @pattern: 总页url模式
    @a: 起始页页数
    @b: 终止页页数
    2016/5/11 00:02 整理完毕
    """
    # 获得总页url数组
    page_urls = get_page_urls(pattern,a,b)
    print "page_urls OK"

    """得到总页的有效信息，以及分页的url"""
    info=get_all_info(page_urls)
    urls=info[3] # 分页url
    # 获得分页信息
    sep_info=get_sep_info(urls)
    print "sep_info OK"

    # 输出
    filename="../info/hong%d_%d.txt"%(a,b)
    f=open(filename,'w')
    for i in range(0,len(info[0])):
        for j in range(0,len(info)):
            info[j][i]=info[j][i].replace("\t","")
            f.write('%s\t'%info[j][i])
        for j in range(0,len(sep_info)):
            print sep_info[j][i]
            sep_info[j][i]=sep_info[j][i].replace("\t","")
            f.write('%s'%sep_info[j][i])
            if j!=(len(sep_info)-1):f.write('\t')
        print i
        f.write('\n')
    f.close()

    print "finish"


pattern="https://book.douban.com/subject/1007305/reviews?score=&amp;start="
get_info(pattern,4,5)
# for i in range(2,6):
#     get_info(pattern,i*10,(i+1)*10)
#     print i*10,(i+1)*10
#     time.sleep(61) #沉睡1分钟以上

# get_info(pattern,2,4) 

# 不存在该页面
# get_sep_info(["https://book.douban.com/review/4970960/"])

