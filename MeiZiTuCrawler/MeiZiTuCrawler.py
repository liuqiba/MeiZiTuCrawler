
#!/usr/bin/env python
# coding=utf-8

import os
import time
import threading
from multiprocessing import Pool, cpu_count
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

DIR_PATH = r"E:\mmjpg"      # 下载图片保存路径


def save_pic(pic_src, pic_cnt):
    """ 将图片下载到本地文件夹
    """
    try:
        img = requests.get(pic_src, headers=HEADERS_2, timeout=30)
        imgname = "pic_cnt_{}.jpg".format(pic_cnt + 1)
        with open(imgname, 'ab') as f:
            f.write(img.content)
            #print(img.content)
    except Exception as e:
        print(e)

def make_dir(folder_name):
    """ 新建套图文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False

'''
def delete_empty_dir(dir):
    """ 如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的情况
    但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹
    """
    if os.path.exists(dir):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                path = os.path.join(dir, d)     # 组装下一级地址
                if os.path.isdir(path):
                    delete_empty_dir(path)      # 递归删除空文件夹
        if not os.listdir(dir):
            os.rmdir(dir)
            print("remove the empty dir: {}".format(dir))
    else:
        print("Please start your performance!")     # 请开始你的表演


lock = threading.Lock()     # 全局资源锁


def urls_crawler(url):
    """ 爬虫入口，主要爬取操作
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10).text
        # 套图名，也作为文件夹名
        folder_name = BeautifulSoup(r, 'lxml').find(
            'h2').text.encode('ISO-8859-1').decode('utf-8')
        with lock:
            if make_dir(folder_name):
                # 套图张数
                max_count = BeautifulSoup(r, 'lxml').find(
                    'div', class_='page').find_all('a')[-2].get_text()
                # 套图页面
                page_urls = [url + "/" + str(i) for i in
                             range(1, int(max_count) + 1)]
                # 图片地址
                img_urls = []
                for index, page_url in enumerate(page_urls):
                    result = requests.get(
                        page_url, headers=HEADERS, timeout=10).text
                    # 最后一张图片没有a标签直接就是img所以分开解析
                    if index + 1 < len(page_urls):
                        img_url = BeautifulSoup(result, 'lxml').find(
                            'div', class_='content').find('a').img['src']
                        img_urls.append(img_url)
                    else:
                        img_url = BeautifulSoup(result, 'lxml').find(
                            'div', class_='content').find('img')['src']
                        img_urls.append(img_url)

                for cnt, url in enumerate(img_urls):
                    save_pic(url, cnt)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    urls = ['http://mmjpg.com/mm/{cnt}'.format(cnt=cnt)
            for cnt in range(1, 953)]
    #pool = Pool(processes=cpu_count())
    for url in urls:
        urls_crawler(url)
    try:
        delete_empty_dir(DIR_PATH)
        #pool.map(urls_crawler, urls)
    except Exception as e:
        time.sleep(30)
        delete_empty_dir(DIR_PATH)
        #pool.map(urls_crawler, urls)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''
HEADERS_2 = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.930mh.com"
}
real_url = 'http://www.930mh.com'
u = 'http://www.930mh.com/manhua/1532/'

base_url = 'http://mhimg.acg.gd:22122/images/comic/102/{ccc}/'
def find_all_chapters(url):
    _requests = requests.get(url)
    _content = _requests.text
    _bs = BeautifulSoup(_content,'lxml')
    tag_li_list = _bs.find("ul",id='chapter-list-1').find_all('li')
    url_list=[]
    li_count=0
    for tag in tag_li_list:
        try:
            file_name = tag.find("span",class_="list_con_zj").text.strip()
            li_count = li_count+1
            if(make_dir(file_name)):
                url_list.append( tag.find('a')['href'])
                print(tag.find('a')['href'])
                print(tag.find("span",class_="list_con_zj").text.strip())
            
                #对应章节的所有漫画图片

                chatpter_page_content = requests.get(real_url+tag.find('a',)['href']).text
                #chatpter_bs.find("script",text=re.compile(r"var chapterImages = '(.*?)';$", re.MULTILINE | re.DOTALL))
            
                chatpter_bs = BeautifulSoup(chatpter_page_content,'lxml')

                #img_list = chatpter_bs.find_all("script",attrs = re.compile(r"[0-9 a-z]*\.jpg"))
                #img_list = chatpter_bs.find_all("script",text = re.compile(r"[0-9 a-z]*\.jpg",re.MULTILINE | re.DOTALL))
                #print(str(chatpter_bs.text))
                img_list_text = chatpter_bs.find("script",text = re.compile(r"[0-9 a-z]*\.jpg",re.MULTILINE | re.DOTALL))
                #for x in img_list:
                #    print(x.text)
                img_list =  re.compile(r"\"[0-9 a-z]{1,}\.jpg").findall(str(img_list_text))
            
                _murl = base_url.format(ccc = str(203305+li_count))
                
                count = 0
                for img_str in img_list:
                    #print(str(img_str)[1:])
                
                    img_url = _murl+str(img_str)[1:]
                    print(img_url)
                    count+=1
                    save_pic(img_url,count)
                
        except Exception as e:
            print(e)
       
        
    
            

url = "http://www.930mh.com/manhua/1532/389349.html#p=2"
find_all_chapters(u)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#def urls_crawler(url):
    
#        #1获取链接text
#        #2通过bs解析text
#        #3找到对应需求内容
   
#    r = requests.get(url,headers = HEADERS,timeout=10).text
#    bs = BeautifulSoup(r,'lxml')
#    #bbs = bs.find('meta',class_ = 'meta')BeautifulSoup(r, 'lxml').find('meta', property="og:image")['content']
#    bbs = BeautifulSoup(r, 'lxml').find('meta', property="og:image")['content']
#    print(bbs)

#    imgR = requests.get(bbs,headers = HEADERS,timeout=10)

#    make_dir("ttt")
#    with open(DIR_PATH,'ab') as f:
#        f.write(img.content)
   
#''

#urls_crawler(url)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







































































