#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:26:19 2020

@author: ptck
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:55:07 2019

@author: ptck
"""


# coding: utf-8

# In[1]:


import sys, traceback, time
#from os import environ
from os import chdir
from os import makedirs
import warnings
import csv
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
#import os
#import pandas as pd
#from pandas import DataFrame, Series, read_csv

#from multiprocessing import Pool
from urllib import parse
#from functools import partial

import datetime


Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y/%m/%d/%H')

origin_input_path='./dbproj/includes/'
origin_output_path='./output/%s/'%(DATE)

try :
	
    makedirs(origin_output_path)
except:
   pass

def read_file(filename) :
    origin_input_path = './dbproj/includes/'
    # csv file 읽기 위함
    f = filename
    models = dict()
    with open(origin_input_path+f, 'r', newline='') as file:
        models['keyword']=[]
        models['model']=[]
        for num,line in enumerate(file.readlines()):
            # 0번째에는 품목명이니까 제외
            lines = line.split(',')[1:]
            # 0,1 row에는 필요없는 정보
            if num <=1:
                continue
            # 키워드가 빈 스트링일 경우 더이상 키워드 없음
            if lines[0]=='':
                break
            
            # keyword 삽입
            models['keyword'].append(lines[0])
            # 모델명만 가져오기 위함
            try :
            
                a = lines.index('')
                models['model'].append(lines[1:a])
            except:
                models['model'].append(lines[1:])
                
            
    #print(csv_data)
    return models

# In[3]:
# k는 TV,건조기와 같은 것들, name은 순위를 알아야하는 모델명


def BS_url(k,a):
    # k 는 키워드값 , a 는 page index
    
    url='https://search.shopping.naver.com/search/all.nhn?origQuery={}&pagingIndex={}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={}'.format(k,a,k)            
        
    text = None
    while text is None :
        print('[%s] GET>> %s'%(str(datetime.datetime.now()), url))
        try :
            res = requests.get(url,verify=False, timeout=5)
            text = res.text
        except :
            pass
        time.sleep(1)
    soup = BeautifulSoup(text,'html.parser')
    return soup


def Info_get(s):
    # s 는 위의 soup값을 의미 , N 은 순위 매기기위한 값 
    # url에서 각종 정보를 받아오는 역할
    srank = s.find_all("li",{"class":"_itemSection"})
    Title_1=[]
    RANK=[]
    srank_v = []
    review=[]
    # select 는 최저가라고 써있는 네이밍만 골라내기위한 선택적 요소
    select = []
        
    for n in srank:
        # 광고를 제외하기 위한 값
        L=n.get("data-expose-area")
        if not L in ['lst*B','lst*H']  :
                
           

                
            #te는 제품 이름 따온거
            te = n.find("div",{"class":"tit"})
            #org는 쇼핑몰최저가만을 오가닉순위에 넣기위한 값
            org = n.find("p",{"class":"mall_txt"})
            srank_v.append(n.find_all("span",{"class":"etc"}))
            P = te.text
            P = P.replace(' ','').replace('\xa0','').replace('\n','').replace('\r','')
            Title_1.append(P.upper())
            N = n.get("data-expose-rank")
            RANK.append(N)
            select.append(org.text.replace('\n','').replace(' ',''))
        
            
    for m in range(len(srank_v)):
        # 리뷰수 따오기
        review.append(srank_v[m][1].find("em").text)
    Title=Title_1
    return RANK, Title , select, review

def trans_str(a):
    return a.upper().replace(' ','').replace('\r','').replace('\n','').replace('\xa0','')

def organic_rank(k,name):
    
    # inde_1은 랭크값을 임시로 보관, inde_2는 리뷰수, inde_3는 모델명을 찾은 순서대로 보관하는 용도
    # N은 랭크값을 부여하기위한 상수
    inde_1=[]
    inde_2=[]
    inde_3=[]
    # name_1 은 선택된 모델들을 제거하기 위한 하나의 바구니
    name_1=name.copy()
    
    for a in range(1,26):
        
        if len(name_1)==0:

            break
        soup = BS_url(k,a)
        # 일단 모든 값들 가져온다.
        rank = Info_get(soup)[0]
        Title = Info_get(soup)[1]
        select = Info_get(soup)[2]
        review = Info_get(soup)[3]
        
        
        # name_2는 모델명들을 비교하기 위한 일시적인 바구니
        for i in range(len(Title)):
            name_2=name_1.copy()
            for x,y in enumerate(name_2):
                
                # name_3는 name_2의 각 원소들을 하나씩 꺼내서 비교해보기위한 값
                name_3=name_2[x]
                try: 
                    name_4 = y.replace('삼성전자','삼성')
                except:
                    name_4 = y


                if (trans_str(y) in Title[i] and select[i]=='최저가있음') or (trans_str(name_4) in Title[i] and select[i]=='최저가있음'):
                
                    inde_1.append(rank[i])
                    inde_2.append(review[i])
                    inde_3.append(name.index(y))
                    name_1.remove(name_3)
                    name[name.index(y)]=name[name.index(y)].replace(name[name.index(y)],'none')
                    break
                
        
        
            if len(name_1)==0:
                break
    
    if len(name_1)!=0:
        for p in name_1:
            na = name.index(p)
            name[na]=name[na].replace(name[na],'none')
            inde_3.append(na)
            
            
            inde_1.append('{}은 순위권 밖'.format(p.replace('\xa0',' ')))
            inde_2.append('{}은 순위권 밖'.format(p.replace('\xa0',' ')))
    
    
    RANK = []
    REVIEW = []
    i=0
   
    
    for l in range(len(inde_3)):
        c = inde_3.index(l)
        RANK.append(inde_1[c])
        REVIEW.append(inde_2[c])
    
    
    
    return RANK,REVIEW


# In[4]:

def or_final(csv):
	
    start_time = time.time()
    L = read_file(csv)
    P = []
    for i in range(len(L['keyword'])):
        P.append(organic_rank(L['keyword'][i], L['model'][i] ))
    print(time.time() - start_time)    
    return P


# In[5]:

# 크롤링을 통한 쇼핑검색 탐색
print('Start')
A = or_final('Naver_0305.csv')

# In[8]:

def model_name(key_model,A):
    All = []
     # 모델명들을 하나의 리스트에 넣어진 리스트 a, 각 모델들의 키워드를 넣은 리스트 b   
    Model = []
    Keyword = []
    N=[]
    for i,j in enumerate(key_model['keyword']):
        m = j.replace('\xa0',' ')
        n = key_model['model'][i]
        L = []
        for k in n:
            while True:
                if '\xa0' in k :
                    k=k.replace('\xa0',' ')
                    continue
                else:
                    L.append(k)
                    break
        All += [[m] + L]
        All += [['rank']+A[i][0]]
        All += [['review']+A[i][1]]


    return All

Final = model_name(read_file('Naver_0305.csv'),A)

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

with open(origin_output_path+'Nshop_Organic_Rank.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile,dialect='mydialect')
    for row in Final:
        thedatawriter.writerow(row)


    