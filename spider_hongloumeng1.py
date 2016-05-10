# -*- coding:utf-8 -*-
import urllib2 # 使用header
import re # 正则
import time # 延时
import traceback # 错误判断

def get_page_urls(str,a,b):
    """
    获得每一页的url
    https://book.douban.com/subject/1007305/reviews?score=&amp;start=25
    @str:"https://book.douban.com/subject/1007305/reviews?score=&amp;start="
    @n:总共的页数
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

def get_first_info(info):
    """ 
    获得该总页信息：
    标题、链接、姓名、时间
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



def get_all_urls(urls):
    """
    获得所有的urls
    @urls:为page_urls的数组
    @return：urls,titles,names,star,time,num,respon
    """
    comment_urls=[]
    titles=[]
    name=[]
    time=[]
    i=0
    for url in urls:
        print(url)
        html=get_content(url)
        info=get_first_info(html)
        comment_urls.extend(info[1])
        titles.extend(info[0])
        name.extend(info[2])
        time.extend(info[3])
        print "page=%d"%i
        i += 1
        print titles[0],name[0],time[0],comment_urls[0]
    return titles,name,time,comment_urls

def get_sep_info(urls):
    print "get_sep_info"
    star=[];good=[];total=[];comments=[];i=0;respons=[]
    for url in urls:
        print url,i
        goods="NA";totals="NA";comment="NA";stars="NA";respon="NA"
        html=get_content(url)
        regex_star=r'<span title="(.+?)">'
        pat_star = re.compile(regex_star)
        regex_judge=r'<em id=(.+?)</em>'
        pat_judge=re.compile(regex_judge)
        regex_comment=r'<span property="v:description" class="">(.+?)<div class="clear"></div></span>'
        pat_comment=re.compile(regex_comment)
        regex_respon=r'<div class="bd">(.)'
        pat_respon=re.compile(regex_respon)

        try: 
            stars=re.findall(pat_star,html)
        except:
            print "no page"
            star.append(stars)
            good.append(goods)
            total.append(totals)
            respons.append(respon)
            comments.append(comment)
            continue
        if len(stars)==0: 
            stars="NA"
        else:
            stars=stars[0]
        try:
            goods=re.findall(pat_judge,html)[0].split(">")[1]
        except:
            print "NO PAGE"
            print stars,goods,totals,respon,comment
            star.append(stars)
            good.append(goods)
            total.append(totals)
            respons.append(respon)
            comments.append(comment)
            print len(star),len(good),len(total),len(respons),len(comments)
            continue
        totals=re.findall(pat_judge,html)[1].split(">")[1]
        if goods=="":goods="NA"
        if totals=="":totals="NA"
        star.append(stars)
        good.append(goods)
        total.append(totals)
        comment=re.findall(pat_comment,html)[0]
        comment=comment.decode('utf-8','ignore').encode('utf-8').strip()
        comments.append(comment)
        respon=str(len(re.findall(pat_respon,html)))
        respons.append(respon)
        i+=1
        if i%5==0:time.sleep(4)
        # print star[0],respons[0],good[0],total[0],comments[0]
    return star,respons,good,total,comments

# n=25
# page_urls="https://book.douban.com/subject/1007305/reviews?score=&amp;start=%d" % (n)

def get_info(pattern,a,b):
    page_urls = get_page_urls(pattern,a,b)
    print "page_urls OK"

    # html=get_content("https://book.douban.com/subject/1007305/reviews")
     
    # comment_urls=get_first_info(html)
    # print type(comment_urls)

    """得到总页的有效信息，以及分页的url"""
    info=get_all_urls(page_urls)
    urls=info[3]
    for i in info:
        print i[14]
        print i[15]
    print len(urls)
    sep_info=get_sep_info(urls)
    print "sep_info OK"

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

    print "ok"

"""得到所有页数的url"""
pattern="https://book.douban.com/subject/1007305/reviews?score=&amp;start="
# get_info(pattern,4,5)
for i in range(4,6):
    get_info(pattern,i*10,(i+1)*10)
    print i*10,(i+1)*10
    time.sleep(61)

# get_info(pattern,2,4) 

# 不存在该页面
# get_sep_info(["https://book.douban.com/review/4970960/"])

