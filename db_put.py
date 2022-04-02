#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 11:23:48 2019

@author: ptck
"""

import mysql.connector
import json
import csv
import time
import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
import db_common as common
import crawling as cr


def read_file_related(filename) :
    # db에 없는 새로운 데이터일 경우
    origin_input_path = './dbproj/includes/'
    # csv file 읽기 위함
    f = filename
    models = []
    with open(origin_input_path+f, 'r', newline='') as file:
        
        for num,line in enumerate(file.readlines()):
            
            lines = line.split(',')
            # 0 row에는 필요없는 정보
            if num <=0:
                continue
            
            # keyword 삽입
            models.append(lines[0].replace('\r','').replace('\n',''))
            # 모델명만 가져오기 위함
            
    return models

def put_related(key,cursor):
    # 처음에 디비에 넣을 때 값
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    #curs = cnx.cursor()
    

    
    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    # 품목 업데이트 됐을 경우에 처음에 넣어줘야함.
    Da_1 = datetime.datetime.now()
    DATE = Da_1.strftime('%Y/%m/%d/%H')
    data = []
    data_2 = {}
    for i,j in enumerate(key):
        #data_2['{}'.format(j)]=df[i]
        #c = data_2['{}'.format(j)]
        #a = (i+1,'{}'.format(j),'related',json.dumps(c,ensure_ascii=False),1,1)
        c = {}
        a = ['{}'.format(j),DATE,DATE]
        data.append(a)

    data=data
    sql = """insert into naver_related_keywords(keyword,created_by,updated_by)
         values (%s, %s, %s)"""
         
         
    cursor.executemany(sql, data)
    cnx.commit()
    
    cnx.close()

    return None

##-----------------------------------------------------------------
    
    
def read_file_search(filename) :
    origin_input_path='./dbproj/includes/'
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
    

def put_keyword_search(models,cursor):
    
    Da_1 = datetime.datetime.now()
    DATE = Da_1.strftime('%Y/%m/%d/%H')    
    keyword = models['keyword']
    sql = """INSERT INTO nshop_search_keywords(keyword, created_by, updated_by)
    VALUES(%s, %s, %s)"""
    data = []
    for i in keyword:
        
        data.append([i, DATE, DATE])

    cursor.executemany(sql,data)
    cnx.commit()
    cnx.close()
    
    return None
    
    
def put_model_search(models,cursor):


    keyword = models['keyword']
    model = models['model']
    data = []

    Da_1 = datetime.datetime.now()
    DATE = Da_1.strftime('%Y/%m/%d/%H')
    sql = """INSERT INTO nshop_search_models (keyword, model, created_by, updated_by)
    VALUES(%s, %s, %s, %s)"""

    #word_id 리스트 불러옴  ### 만약 키워드가 추가 되어서 이값이 늘어나도 상관없음 길이만큼 적용이라
    
    for index,mo_all in enumerate(model) : #TV [...models....] 이렇게 뽑혀나옴

        for ind,mo in enumerate(mo_all) :
            
            #뽑혀나온 ₩[models] 하나에서 [wid와 모델명하나]를 뽑아옴

            data.append([keyword[index], mo, DATE, DATE])    # model_name에 .strip() 함수를 추가해줌. \n \w 없애줌


    #curs.executemany(sql, [(w,) for w in map(lambda t: t[0], data)])
    cursor.executemany(sql, data)
    cnx.commit()
    cnx.close()

    return None


def put_Table_search(cursor):

    keyword = common.get_nkey_func(cursor)
    sql = '''INSERT INTO nshop_search_records (day_id, keyword, model, rank_id, is_organic, reviews, is_price, created_by, updated_by)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    
    Da_1 = datetime.datetime.now()
    DATE = Da_1.strftime('%Y/%m/%d/%H')
    day = Da_1.strftime('%Y%m%d')   #참조테이블이 돌아가서 저장이 된 후 디비를 넣는거라 시간 간격이 있을듯. 그냥 14시로 고정??
    #k는 키워드 하나씩 받음 ex)"TV" return 값은 랭크,품목명,리뷰수,최저가 순으로 4개

    #위에 원래는 w=1 이였음. 만약 auto_increment되면 w값 어팬드 안해도 자동으로 들어갈듯.
    #나중에 디비에서 w(즉 ref테이블의 id)에 자동증가 속성 추가 성공하면 w빼는 작업 필요할듯
    for i in keyword:
        
        raw_data = cr.ref_Table(i)   #i로 TV가 하나 들어가면 30페이지 까지의 참조 데이터 가져오기
        data =[]
        
        for m in raw_data: # m는 오가닉아이템 긁어온 1000개만큼 돌리는거임

            # 키워드 하나당, len(item_rank) 만큼 돌면서 밑에 값을 다 채워 넣음)
            #### 첫번째 1 이 프라임키라서 이거 다 다른 값 넣어줘야 함.... 으엉...
            data.append([day, m[0], m[1], m[2], m[3], m[4], m[5], DATE, DATE])
        cursor.executemany(sql, data)  #
        cnx.commit()                #
        data.clear()                 #
        print("진행중..."+i+"완료...")


        #id 는 계속 증가해야되고, wid는 (214....)와 맞물려 있는 값이고, day는 고정값, hour 고정값, 뒤에는 받아오기

        # word_id 가 key는 Mul 인데, index는 unique임....
        # day, hour 도 uniqe index로 설정되어있다.

    #curs.executemany(sql, data)
    # 나중에 data를 3만개 다 리스트에 넣고 익스큐트 하지말고 천개 넣고 익스큐트하고 이런식으로 변경필요
    #conn.commit()
    cnx.close()

    return None















