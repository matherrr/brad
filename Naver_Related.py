#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys, traceback, time
from os import environ
import os
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup

import pandas as pd
from pandas import DataFrame, Series

from multiprocessing import Pool
from urllib import parse
from functools import partial
import datetime
from os import environ
from os import chdir



# In[4]:
a = datetime.datetime.now()
b = a.strftime('%Y/%m/%d/%H')
c = b.replace("/","/")


origin_input_path = './dbproj/includes/'
origin_output_path = './output/%s'%(d)



# 키워드 읽어 오는 함수 (미디어에서 요청하는 키워드들을 불러온다)
def get_links_df(csv):
    df = pd.read_csv(origin_input_path+csv)
    keywords = df['Keyword']
       
    return keywords


# 하나의 키워드에 대해 연관검색어를 가져오는 함수
def get_related_list(k):
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={}'.format(k)
    verify=False
    res = requests.get(url)
    text = res.text
    soup = BeautifulSoup(text,'html.parser')
              
    
    if soup.find("ul",{"class":"_related_keyword_ul"}) :
        
        srank_soup = soup.find("ul",{"class":"_related_keyword_ul"})
        text = srank_soup.text
        re_text  = text.replace('   ', ',').replace('  ','')
        list_related = re_text.split(',')   # 해당 i번째의 연관검색어 리스트가 뽑힘. (리스트 길이는 다 다름)
    else :
        list_related = ['연관검색어 없음']
    
    return list_related


# get_related_list 함수를 이용하여 각 키워드에 대한 모든 연관검색어를 저장하는 함수
def make_related_listed():
    
    keywords = get_links_df('keyword_0819.csv').tolist()
    
    related_lists=[] #각 키워드에 대한 연관검색어 리스트를 한덩어리로 저장. 140개 키워드가 있으면 140개 리스트덩어리가 담김
    
    for i in keywords:
        print("====="+i+"=====")
        re_list = get_related_list(i)
        related_lists.append(re_list)
          
    return related_lists    


# 완성된 테이블을 만드는 함수 
def Make_Table():
    start_time = time.time()
    keywords = get_links_df('keyword_0819.csv').tolist() # 키워드 140를 불러옴

    related_lists = make_related_listed() # 키워드에 해당하는 140개에 해당되는 리스트 뭉치들을 불러옴
    
    concat_list=[]  # 1개의 키워드와 그에 해당하는 연관검색어를 합친 테이블을 총 140개 담는다. -> 합치려고
    
    for i in range(len(keywords)):
        
        k_pd = pd.Series(keywords[i])
        K_pd = pd.DataFrame(k_pd, columns=['키워드'])
        L_pd = pd.DataFrame(related_lists[i],columns=['연관검색어'])
        
        table = pd.concat([K_pd, L_pd], axis=1)
        table.fillna(value ='', inplace=True)
        
        concat_list.append(table)
        
    
    F_Table = pd.concat(concat_list)   # 140개의 테이블을 합쳐 하나의 테이블로 만든다.
    F_Table = pd.DataFrame(F_Table)
    print(time.time() - start_time)
    return F_Table    






# In[10]:

Make_Table().to_csv(origin_output_path+'Naver_Related.csv', sep=',', encoding='euc-kr', index=True)



# In[ ]:





