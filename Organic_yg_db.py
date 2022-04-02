
"""
Created on Mon Mar 17 15:30:07 2020

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
import mysql
import mysql.connector
import requests
from bs4 import BeautifulSoup
#import os
#import pandas as pd
#from pandas import DataFrame, Series, read_csv

#from multiprocessing import Pool
from urllib import parse
#from functools import partial
import json
import datetime

Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y/%m/%d/%H')
origin_input_path='./dbproj/includes/'
origin_output_path='./output/%s/'%(DATE)

try :
    makedirs(origin_output_path)
except:

    pass


def get_key_list():
    # db 에서 키워드 가져오기
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    mysql_conf = {
        'host': 'stage.pengtai.co',
        "port" : 3306,
        'db': 'monitoring',
        'user': 'db-worker',
        'password': 'vjdxkdlzhfldk/2020#'
    }
    cnx = mysql.connector.connect(**mysql_conf)
    curs = cnx.cursor()
    sql = "SELECT id,word FROM nshop_search_keywords ORDER BY id"
    curs.execute(sql)
    Word = [i[1] for i in curs]

    cnx.close()
    return Word

def get_model_list(word):
    
    # db 에서 찾아야 하는 모델들
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    mysql_conf = {
        'host': 'stage.pengtai.co',
        "port" : 3306,
        'db': 'monitoring',
        'user': 'db-worker',
        'password': 'vjdxkdlzhfldk/2020#'
    }
    cnx = mysql.connector.connect(**mysql_conf)
    curs = cnx.cursor()
    sql = "SELECT id,models FROM nshop_search_keywords where word='{}'".format(word)
    curs.execute(sql)
        
    mod = [json.loads(i[1]) for i in curs][0]
    
    model = [j['name'] for j in mod]
    cnx.close()
    return model


def trans_str(a):
    return a.strip().upper().replace('\r','').replace('\n','').replace('\xa0',' ').replace('  ',' ')
    

def get_items_list(model):
    # db에서 키워드당 1000개씩 가져오기
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    mysql_conf = {
        'host': 'stage.pengtai.co',
        "port" : 3306,
        'db': 'monitoring',
        'user': 'db-worker',
        'password': 'vjdxkdlzhfldk/2020#'
    }
    cnx = mysql.connector.connect(**mysql_conf)
    curs = cnx.cursor()
    
    Title = []
    RANK = []
    review = []
    Da_1 = datetime.datetime.now()
    da = Da_1.strftime('%Y%m%d')
    
    sql = "SELECT rank_id, title, reviews FROM nshop_search_record_items where keyword='{}' and is_ad=0 and (area='C' or area='N') and record_id=(SELECT MAX(id) FROM nshop_search_records WHERE keyword = '{}' and status_code = 200 and pages=40 and day_id ={} ) ".format(model,model,da)
    curs.execute(sql)
    for j in curs:
        Title.append(trans_str(j[1]))
        RANK.append(j[0])
        review.append(j[2])

    cnx.close()
    return Title, RANK, review


def split_name(name):
    c = []
    while True:
        
        try :
            name.index(' ')
            b = name[:name.index(' ')]
            c.append(b)
            
            try :
                
                name = name.replace(b+' ','')

            except:
                name = name.replace(b,'')

        except:
            c.append(name)
            break
    return c

def name_name(name_1,name_2):
    
    for i in name_1:
        if i in name_2:
            continue
        else:
            return False
    return True


def organic_rank(keyword,name):
    
    # inde_1은 랭크값을 임시로 보관, inde_2는 리뷰수, inde_3는 모델명을 찾은 순서대로 보관하는 용도
    # N은 랭크값을 부여하기위한 상수
    inde_1=[]
    inde_2=[]
    inde_3=[]
    # name_1 은 선택된 모델들을 제거하기 위한 하나의 바구니
    name_1=name.copy()


    L = get_items_list(keyword)
    Title = L[0]
    rank = L[1]
    review = L[2]
        
        
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


            if (name_name(split_name(trans_str(y)),split_name(Title[i]))== True) or (name_name(split_name(trans_str(name_4)),split_name(Title[i]))== True):
                
                inde_1.append(rank[i])
                inde_2.append(review[i])
                inde_3.append(name.index(y))
                name_1.remove(name_3)
                name[name.index(y)]=name[name.index(y)].replace(name[name.index(y)],'none')
                break
                
    if len(name_1)!=0:
        for p in name_1:
            na = name.index(p)
            name[na]=name[na].replace(name[na],'none')
            inde_3.append(na)
            inde_1.append(int('-1'))
            inde_2.append('-1')

    
    RANK = []
    REVIEW = []
    i=0
   
    
    for l in range(len(inde_3)):
        c = inde_3.index(l)
        RANK.append(inde_1[c])
        REVIEW.append(inde_2[c])
    
    
    
    return RANK,REVIEW


# In[4]:



def or_final(keyword):
	# key 는 키워드들을 모두 가지고 있는 한개의 리스트
    start_time = time.time()
    
    P = []
    for i,j in enumerate(keyword):
        P.append(organic_rank(j, get_model_list(j)))
    print(time.time() - start_time)    
    return P


# In[5]:

# 크롤링을 통한 쇼핑검색 탐색
print('Start')
keyword = get_key_list()
A = or_final(keyword)

# In[6]:

def model_name(keyword,A):
    All = []
     # 모델명들을 하나의 리스트에 넣어진 리스트 a, 각 모델들의 키워드를 넣은 리스트 b   
    Model = []
    Keyword = []
    N=[]
    for i,j in enumerate(keyword):
        m = j.replace('\xa0',' ')
        n = list(get_model_list(keyword[i]))
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


final = model_name(keyword,A)
csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)



with open(origin_output_path+'Nshop_Organic_Rank_db.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile,dialect='mydialect')
    for row in final:
        thedatawriter.writerow(row)



