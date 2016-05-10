# -*- coding:utf-8 -*-
import urllib2
import re
import socket
   
"""
抓取时碰到403问题
"""
   
def bound_socket(*a, **k):  
    sock = true_socket(*a, **k)  
    sock.bind((ipbind, 0))  
    return sock  


def get_content(url):
    """doc."""

    req=urllib2.Request(url)

    req.add_header("user-agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36")
    req.add_header("GET",url)
    req.add_header("host","book.douban.com")

    html=urllib2.urlopen(req,timeout=15)
    content=html.read()
    html.close()

    return content

def get_urls(info):
    """ doc.
      <a id="af-1409002" href="https://book.douban.com/review/1409002/" class="j a_unfolder" style="background:none;">um/w%3D580/sign=269396684d4a20a4311e3ccfa0539847/0aa95edf8db1cb132cd1f269df54564e92584b15.jpg" pic_ext="jpeg"  width="510" height="765">
      @info:html内容
    """
    regex=r'href="(.+?)" class="j a_unfolder"'
    pat = re.compile(regex)
    regex_title=r'<a title="(.+?)"'
    pat_title=re.compile(regex_title)
    regex_name=r'class=" ">(.+?)</a>'
    pat_name=re.compile(regex_name)
    regex_time=r'<span class="">(.+?)</span> &nbsp; &nbsp;'
    pat_time=re.compile(regex_time)
    regex_respon=r'"">(.+?)回应</span>'
    pat_respon=re.compile(regex_respon)

    comment_urls=re.findall(pat,info)
    comment_titles=re.findall(pat_title,info)
    comment_name=re.findall(pat_name,info)
    comment_time=re.findall(pat_time,info)
    comment_respon=re.findall(pat_respon,info)

    for i in range(0,len(comment_respon)):
        comment_respon[i]=str(comment_respon[i])
    
    # i=0
    # for comment_url in comment_titles:
    #     i+=1
    #     print comment_url,i

    return comment_titles,comment_urls,comment_name,comment_time,comment_respon

def get_page_urls(str,n):
    """
    获得每一页的url
    https://book.douban.com/subject/1007305/reviews?score=&amp;start=25
    @str:"https://book.douban.com/subject/1007305/reviews?score=&amp;start="
    @n:总共的页数
    """
    page_urls=[]
    for i in range(0,n):
        page_urls.append("%s%d" % (str,i*25))
        #print i
    return page_urls

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
    respon=[]
    i=0
    for url in urls:
        html=get_content(url)
        info=get_urls(html)
        comment_urls.extend(info[1])
        titles.extend(info[0])
        name.extend(info[2])
        time.extend(info[3])
        respon.extend(info[4])
        print "page=%d"%i
        i += 1
    return titles,name,time,respon,comment_urls

def get_sep_info(urls):
    print "get_sep_info"
    star=[];good=[];total=[];comments=[];i=0
    for url in urls:
        goods="";totals="";comment="";stars=""
        html=get_content(url)
        regex_star=r'<span title="(.+?)">'
        pat_star = re.compile(regex_star)
        regex_judge=r'<em id=(.+?)</em>'
        pat_judge=re.compile(regex_judge)
        regex_comment=r'<span property="v:description" class="">(.+?)<div class="clear"></div></span>'
        pat_comment=re.compile(regex_comment)

        stars=re.findall(pat_star,html)
        if len(stars)==0: 
            stars="NA"
        else:
            stars=stars[0]
        star.append(stars)
        goods=re.findall(pat_judge,html)[0].split(">")[1]
        totals=re.findall(pat_judge,html)[1].split(">")[1]
        if goods=="":goods="NA"
        if totals=="":totals="NA"
        good.append(goods)
        total.append(totals)
        comment=re.findall(pat_comment,html)[0]
        comment=comment.decode('utf-8','ignore').encode('utf-8').strip()
        comments.append(comment)
        print i;i+=1
    return star,good,total,comments

# n=25
# page_urls="https://book.douban.com/subject/1007305/reviews?score=&amp;start=%d" % (n)

true_socket = socket.socket  
   
# ipbind='xx.xx.xxx.xx'  
# socket.socket = bound_socket 

"""得到所有页数的url"""
pattern="https://book.douban.com/subject/1007305/reviews?score=&amp;start="
page_urls = get_page_urls(pattern,1)
print "page_urls OK"

# html=get_content("https://book.douban.com/subject/1007305/reviews")
 
# comment_urls=get_urls(html)
# print type(comment_urls)

"""得到总页的有效信息，以及分页的url"""
info=get_all_urls(page_urls)
urls=info[4]
print len(urls)
#sep_info=get_sep_info(urls)
#print "sep_info OK"

# f=open("../info/hong.txt",'w')
# for i in range(0,len(info[0])):
#     for j in range(0,len(info)):
#         f.write('%s\t'%info[j][i])
#     for j in range(0,len(sep_info)):
#         f.write('%s'%sep_info[j][i])
#         if j!=(len(sep_info)-1):f.write('\t')
#     print i
#     f.write('\n')
# f.close()

# print "ok"






