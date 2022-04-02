#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:23:13 2020

@author: ptck
"""

import requests
import warnings
import time
import os
import csv
from urllib import parse
import mysql.connector
from mysql.connector import Error
import datetime
import json

#os.chdir('/Users/ptck/Downloads/')
Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y/%m/%d/%H')

origin_input_path='./dbproj/includes/'
origin_output_path='./output/%s/'%(DATE)

try:

    os.makedirs(origin_output_path)
except:
    pass



def read_file(filename) :
    # db에 없는 새로운 데이터일 경우
    origin_input_path = './dbproj/includes/'
    # csv file 읽기 위함
    f = filename
    S_models= {}
    X_models= {}
    group = {}
    group_name={}
    S_group = []
    X_group = []
    x = 0
    with open(f, 'r', newline='') as file:
        
        
        #print(file.readlines())
        #j=len(file.readlines())-1
        k = 0
        
        for num,line in enumerate(file.readlines()):
            
            if num ==0:
                k+=1
                continue
            
            lines = line.split(',')
            
            #print(lines)
            #print('1111')
            #0 row에는 필요없는 정보
            if lines[0] == '경쟁사' and lines[1]!= '':
                group['none']=[]
            
            if lines[1] != '':
                group[lines[1]] = []
                name = lines[1]
                group_name[name]=[0]
            group[name].append( lines[2].replace('\r','').replace('\n','') )
    L = list(group.keys()).index('none')
    group.pop('none')
    return group, group_name, L




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
    while value == 40 :

        sql = "SELECT count(*) FROM nshop_search_records where word_id={} and day={} and hour={} and item_rank < '41'".format(model,DA,hour)
        curs.execute(sql)
        value = [ j for j in curs][0][0]
        hour = hour - 2
        continue
    sql = "SELECT item_name, low_price FROM nshop_search_records where word_id={} and day={} and hour={} and item_rank <'41' ".format(model,DA,hour)
    curs.execute(sql)        
    blank=[]
    Title = []
    select = []
    for i in curs:
        blank.append(i)
        if len(blank)==0:
            break
        
        Title.append(i[0].upper().replace('\n','').replace('\r','').replace('\xa0','').replace(' ',''))

        select.append(i[1])
    
    if len(blank)==0:
        sql = "SELECT item_name, low_price FROM nshop_search_records where word_id={} and day = {} and item_rank<'41' ".format(model,DA)
        curs.execute(sql)
        for i in curs:
            Title.append(i[0].upper().replace('\n','').replace('\r','').replace('\xa0','').replace(' ',''))

            select.append(i[1])
    
    cnx.close()
    #rows = curs.fetchall()
    
    return Title, select

def organic_check(name):
    
    # inde_1은 랭크값을 임시로 보관, inde_2는 리뷰수, inde_3는 모델명을 찾은 순서대로 보관하는 용도
    # N은 랭크값을 부여하기위한 상수
    inde_1=[]
    inde_2=[]
    inde_3=[]
    # name_1 은 선택된 모델들을 제거하기 위한 하나의 바구니
    group=name[0].copy()
    group_name = name[1]
    num = name[2]
    #for a in range(1,26):
        
        #if len(name_1)==0:

        #    break
        
        #soup = BS_url(k,a)
        # 일단 모든 값들 가져온다.

    L = get_items_list('7')

    Title = L[0]
    select = L[1]

    S_num = 0
    X_num = 0    
    N = {}   
        # name_2는 모델명들을 비교하기 위한 일시적인 바구니
    for i,j in enumerate(Title):
        
        for k in group:
            
            
            for m in group[k]:
                
                if (m in j) and (select[i] =='최저가있음') :
                    group_name[k][0]+=1
            
        
    return group_name, num

def transform(check):
    
     # 모델명들을 하나의 리스트에 넣어진 리스트 a, 각 모델들의 키워드를 넣은 리스트 b   
     
    group = check[0]
    num = check[1]
    All=[]
    
    
    for i,j in enumerate(group):
        
        if i <num:
            m = '당사'
            
            All+= [[m] + [j] + group[j]]
            
        else:
            m = '경쟁사'
            
            All+= [[m] + [j] + group[j]]
            


    return All

Final = transform(organic_check(read_file('Naver_note_0123.csv')))

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)



with open(origin_output_path+'Naver_Organic_first_notebook.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile,dialect='mydialect')
    for row in Final:
        thedatawriter.writerow(row)
        
        
        



























