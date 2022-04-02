
"""
Created on Mon Fab 9 10:55:07 2020

@author: ptck
"""

#alter table nshop_search_record_items drop page;
#
#
#alter table nshop_search_record_items drop page;
#alter table nshop_search_record_items drop `index`;
#alter table nshop_search_record_items drop data;
#alter table nshop_search_record_items drop `rank`;
#
#
#alter table nshop_search_record_items add review int(10) default null;
#alter table nshop_search_record_items add rnk_id int(10) default null;
#
#
#alter table nshop_search_record_items modify review int(10) after record_id;
#alter table nshop_search_record_items modify rnk_id int(10) after record_id;


#alter table nshop_search_records modify day int(10)

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
    # db 에서 키워드 및 번호 가져오기
    mysql_conf = {
        'host': 'localhost',
        'db': 'db-project',
        'user': 'brad',
        'password': '1111'
    }
    #mysql_conf = _config(filepath='./database_ubuntu.config.json') -> 이걸로 나중에 대체
    cnx = mysql.connector.connect(**mysql_conf)
    #conn = mysql.connector.connect(**mysql_conf)

    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()
    sql = "SELECT id,word FROM nshop_searches ORDER BY id"
    curs.execute(sql)
    Id =[]
    Word = []
    for i in curs:
        Id.append(i[0])
        Word.append(i[1])
    
    
    cnx.close()
    return Id,Word

def get_model_list(key):
    # db 에서 찾아야 하는 모델들
    
    mysql_conf = {
        'host': 'localhost',
        'db': 'db-project',
        'user': 'brad',
        'password': '1111'
    }
    #mysql_conf = _config(filepath='./database_ubuntu.config.json') -> 이걸로 나중에 대체
    cnx = mysql.connector.connect(**mysql_conf)
    #conn = mysql.connector.connect(**mysql_conf)

    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()

    day = '20200305'
    sql = "SELECT id, name FROM nshop_search_models where word_id={} and created_by={}".format(key,day)
    curs.execute(sql)
    ind = []
    name = []
    for i in curs:
        ind.append(i[0])
        name.append(i[1])
    cnx.close()
    
    
    return name,ind
    
def trans_str(a):
    return a.strip().upper().replace('\r','').replace('\n','').replace('\xa0',' ').replace('  ',' ')
    

def get_items_list(model):
    # db에서 키워드당 1000개씩 가져오기
    mysql_conf = {
        'host': 'localhost',
        'db': 'db-project',
        'user': 'brad',
        'password': '1111'
    }
    #mysql_conf = _config(filepath='./database_ubuntu.config.json') -> 이걸로 나중에 대체
    cnx = mysql.connector.connect(**mysql_conf)
    #conn = mysql.connector.connect(**mysql_conf)

    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()
    #day = time.strftime('20%y-%m-%d', time.localtime(time.time())) # ex- 191028
    
    DA = time.strftime('%Y%m%d', time.localtime(time.time()))
    #hour = time.strftime('%H', time.localtime(time.time()))

    hour = 6
    value = 0
    
    while value <1044 :

        sql = "SELECT count(*) FROM nshop_search_records where word_id={} and day={} and hour={} ".format(model,DA,hour)
        curs.execute(sql)
        value = [ j for j in curs][0][0]
        hour = hour - 2
        continue
    
    sql = "SELECT item_name, item_rank, item_review, low_price FROM nshop_search_records where word_id={} and day={} and hour={} ".format(model,DA,hour)
    curs.execute(sql)        
    blank=[]
    Title = []
    RANK = []
    review = []
    select = []
    for i in curs:
        blank.append(i)
        if len(blank)==0:
            break
        
        Title.append(trans_str(i[0]))
        RANK.append(i[1])
        review.append(i[2])
        select.append(i[3])
    
    if len(blank)==0:
        sql = "SELECT item_name, item_rank, item_review, low_price FROM nshop_search_records where word_id={} and day = {} ".format(model,DA)
        curs.execute(sql)
        for i in curs:
            Title.append(trans_str(i[0]))
            RANK.append(i[1])
            review.append(i[2])
            select.append(i[3])
    
    cnx.close()
    #rows = curs.fetchall()
    
    return Title, RANK, review, select


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


def organic_rank(key,k,name):
    
    # inde_1은 랭크값을 임시로 보관, inde_2는 리뷰수, inde_3는 모델명을 찾은 순서대로 보관하는 용도
    # N은 랭크값을 부여하기위한 상수
    inde_1=[]
    inde_2=[]
    inde_3=[]
    # name_1 은 선택된 모델들을 제거하기 위한 하나의 바구니
    name_1=name.copy()
    
    #for a in range(1,26):
        
        #if len(name_1)==0:

        #    break
        
        #soup = BS_url(k,a)
        # 일단 모든 값들 가져온다.
    a = key[1].index(k)
    b = key[0][a]
    L = get_items_list(b)
    rank = L[1]
    Title = L[0]
    select = L[3]
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


            if (name_name(split_name(trans_str(y)),split_name(Title[i]))== True and select[i]=='최저가있음') or (name_name(split_name(trans_str(name_4)),split_name(Title[i]))== True and select[i]=='최저가있음'):
                
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



def or_final(key):
	
    start_time = time.time()
    
    P = []
    for i,j in enumerate(key[1]):
        P.append(organic_rank(key,j, get_model_list(key[0][i] )[0]))
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
    for i,j in enumerate(keyword[1]):
        m = j.replace('\xa0',' ')
        n = list(get_model_list(keyword[0][i]))[0]
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

# In[9]:

def into_db_nshop(keyword,A):
    

    mysql_conf = {
        'host': 'localhost',
        'db': 'db-project',
        'user': 'brad',
        'password': '1111'
    }
    #mysql_conf = _config(filepath='./database_ubuntu.config.json') -> 이걸로 나중에 대체
    cnx = mysql.connector.connect(**mysql_conf)
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()
    DA = time.strftime('%Y%m%d', time.localtime(time.time()))
    K = keyword
    mod = []
    nam = []
    for i in K[0]:
        mod.append(get_model_list(i)[0])
        nam.append(get_model_list(i)[1])
    #Da_1 = datetime.datetime.now()
    #DATE = Da_1.strftime('%Y/%m/%d')
    data = []
    for i,j in enumerate(A):
        
        for k,p in enumerate(j[0]):
            
            
            c = (i,int(p), int(j[1][k].replace(',','')), K[0][i], nam[i][k], DA, mod[i][k],K[1][i] )
            data.append(c)

    data = tuple(data)
            

    sql = """insert into nshop_search_record_items(record_id,rnk_id,review,word_id,model_id,created_at,model,keyword) 
                values(%s, %s, %s, %s, %s, %s, %s, %s)"""
         
    curs.executemany(sql, data)
    cnx.commit()
    
    
    cnx.close()
    return

into_db_nshop(keyword,A)



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






'''
K = get_key_list()
mod = []
nam = []
for i in A[0]:
    mod.append(get_model_list(i)[0])
    nam.append(get_model_list(i)[1])
    #Da_1 = datetime.datetime.now()
    #DATE = Da_1.strftime('%Y/%m/%d')
data = []
m = 1
for i,j in enumerate(A):
        
    for k,p in enumerate(j[0]):
            
            
        c = (m, m, p, K[0][i], int(j[1][k].replace(',','')), nam[i][k] )
        data.append(c)
        m+=1
data = tuple(data)


sql = "insert into nshop_search_record_items(record_id, index, rank, word_id, review, model_id) values (%s, %s, %s, %s, %s, %s)"


sql = """insert into nshop_search_record_items(record_id, index, rank, word_id, review, model_id)
         values (%s, %s, %s, %s, %s, %s)"""
         

'''











'''
def transpose(C,P):
    #키워드 모델명들을 가진 column생성 및 csv파일 생성을 위한 함수
    G=pd.DataFrame()
    K=pd.DataFrame()
    K_1=pd.DataFrame()  
    for i in range(0,len(C),2):
    
        if i==len(C)-1:
            break
        else:
            D_2 = pd.DataFrame(['na'])
            D = C[i:i+1]
            F = pd.DataFrame([P[0][i//2]])
            M = pd.DataFrame([P[1][i//2]])
            F_1 = F.append(M)
            M_1 = F_1.append(D)
            D_1 = C[i+1:i+2]
            N = pd.DataFrame([P[1][i//2]])
            D_3 = D_2.append(N)
            N_1 = D_3.append(D_1)
            ### F_2는 모델명 : 오가닉순위, D_4는 빈셀과 리뷰수
            F_2 = M_1.T
            D_4 = N_1.T
            F_2.columns=["model","keyword","organic"]
            D_4.columns=["model","keyword","organic"]
            K = F_2.append(D_4)
            K_1 = pd.concat([K_1,K])
            K_1=K_1.replace('na','')
    
    K_1.to_csv(origin_output_path + 'Nshop_Organic_Rank.csv', sep=',', encoding='euc-kr', index=False,header=True)
    return K_1
'''

# In[11]:
#print(transpose(C,P))