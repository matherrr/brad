import sys, traceback, time
from os import environ
from os import chdir
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame, Series

import csv
from urllib import parse
import os, datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


a = datetime.datetime.now()
b = a.strftime('%Y/%m/%d/%H')
c = b.replace("/", "/")

origin_input_path = './dbproj/includes/'
origin_output_path = './output/%s/' % (c)

try:

    os.makedirs(origin_output_path)
except:
    pass



# 단순히 csv파일 읽어오는 함수
def read_file(filename) :
    f = filename
    with open(f) as file:
        csv_data = []
        for line in file.readlines():
            csv_data.append(line.split(','))
    #print(type(csv_data)) = list type
    return csv_data

# 키워드을 뽑아오는 함수
def read_keyword():
    csv_data = read_file(filename)
    keyword_list =[]
    for i in range(2, len(csv_data)):
        key = csv_data[i][1]
        keyword_list.append(key)

    cut_num = keyword_list.index('')
    keyword_list = keyword_list[:cut_num]

    return keyword_list  #, cut_num


# adver에서는 필요없는 함수. 모델명 불러오는 함수
def read_items():
    csv_data = read_file(filename)
    cut_num_2 = len(read_keyword())
    raw_list = csv_data[2:cut_num_2+2]

    return raw_list


# 하나의 키워드 크롤링 함수
def ad_rank_review(k):
    tlist = [] # 제품명
    tlist2 = [] # 리뷰수
    # col = ['1위','2위','3위','4위','5위','6위','7위','8위']
    for i in range(0, 2):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        url = 'https://search.shopping.naver.com/search/all.nhn?origQuery={}&pagingIndex={}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={}'.format(
            k, i + 1, k)
        res = requests.get(url, verify=False)
        text = res.text
        soup = BeautifulSoup(text, 'html.parser')

        lis = soup.find_all("li", {"class": "ad _model_list _itemSection"})

        for li in lis:

            tit = li.find("div", {"class": "tit"})
            text = tit.text
            tlist.append(text)

            info = li.find("div", {"class": "info"})
            etc = info.find("span", {"class": "etc"})
            em = etc.find("em").text
            tlist2.append(em if 0<len(em) else 0)

    return tlist, tlist2


#print(ad_rank_review('TV')[0]) #광고모델명
#print(ad_rank_review('TV')[1]) #순위

# 다수 키워드 크롤링 자료 병합 및 전처리 해주는 함수
def MakeTable(k):
    start_time = time.time()
    total_list = []
    # 처음 0번째에 1~8위 넣어주기 그리고 포문으로 나머지 넣어주기
    for i in range(0,len(k)):

        list_1 = ad_rank_review(k[i])[0]
        list_1.insert(0,k[i])
        list_1.insert(1,'제품명')


        list_2 = ad_rank_review(k[i])[1]
        list_2.insert(0, k[i])
        list_2.insert(1,'리뷰수')

        total_list.append(list_1)
        total_list.append(list_2)

        print("======="+k[i] +" success=======")

    index = ['','','1위','2위','3위','4위','5위','6위','7위','8위']
    total_list.insert(0, index)
    print(time.time() - start_time)
    return total_list





filename = 'Naver_1001.csv'
k = read_keyword()
print(k)

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)


with open(origin_output_path+'Nshop_Ad_Rank.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    for row in MakeTable(k):
        thedatawriter.writerow(row)