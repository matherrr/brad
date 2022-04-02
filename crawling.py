#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:55:15 2019

@author: ptck
"""


import mysql.connector
import json
import csv
import time

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup

def BS_url(key,a):
    # k 는 키워드값 , a 는 page index
    
    url='https://search.shopping.naver.com/search/all.nhn?origQuery={}&pagingIndex={}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={}'.format(key,a,key)            
        
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


def Info_get(soup):
    # url에서 각종 정보를 받아오는 역할
    srank = soup.find_all("li",{"class":"_itemSection"})
    model=[]
    rnk=[]
    review=[]
    # select 는 최저가라고 써있는 네이밍만 골라내기위한 선택적 요소
    is_price = []
    is_org=[]

    # 변수명 가독성 높이도록 수정 필요할듯 혹은 주석
    for n in srank:
        # 광고를 제외하기 위한 값
        L=n.get("data-expose-area")  # L 왜 따온거?
        #te는 제품 이름 따온거
        te = n.find("div",{"class":"tit"})
        #org는 쇼핑몰최저가만을 오가닉순위에 넣기위한 값
        model.append(te.text.strip().upper())
        N = n.get("data-expose-rank")
        # 광고의 경우 페이지 바뀔때마다 1부터 다시 시작함 랭킹이
        info = n.find("div", {"class": "info"})
        etc = info.find("span", {"class": "etc"})
        em = etc.find("em").text
        rnk.append(N)
        review.append(em if 0 < len(em) else 0)
        # 쇼핑몰별 최저가 있을시에(is_price) 1, 아닐시 0
        # organic(is_organic) 이면 1, 쇼핑광고면 0 (True:1 , False:0)

        if L in ['lst*B']:        # 광고
            is_org.append('0')
            is_price.append('0')
        elif L in ['lst*C']:      # 최저가 있는경우
            is_org.append('1')
            is_price.append('1')
        elif L in ['lst*N']:      # 이벤트 
            is_org.append('1')
            is_price.append('0')
        else:                     # lst*H 경우. 오가닉아님
            is_org.append('1')
            is_price.append('0')
    
    return rnk, model , is_price, review, is_org
    # rnk의 경우 L = lst*B 경우 페이지 넘어갈때마다 계속 1부터 다시 카운팅됨

def ref_Table(keyword):
    
    organic_rank = []
    organic_model = []
    organic_price = []
    organic_review = []
    organic_is_org = []
    
    for i in range(1,31):
        
        All = Info_get(BS_url(keyword,i))
        organic_rank.append(All[0])
        organic_model.append(All[1])
        organic_price.append(All[2])
        organic_review.append(All[3])
        organic_is_org.append(All[4])
    
    return keyword, organic_model, organic_rank, organic_is_org, organic_review, organic_price
    # 리턴값이 keyword하나는 원소값이고 나머지 뒤에는 리스트들로 나옴 -> 수정?
###------------------------------------------------ 
    

def Related(keyword):
    
    # keyword에 따른 연관검색어 크롤링 함수
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={}'.format(keyword)
    res = requests.get(url, headers=headers, verify=False)
    text = res.text
    soup = BeautifulSoup(text,'html.parser')
           
    dl = soup.find("dl")
    srank = soup.find("ul",{"class":"_related_keyword_ul"})
    rlist=[]
    
    if srank:    
        a = srank.find_all("a")
        
        for i in range(len(a)):
        
            atext = a[i].text
            
            rlist.append(atext)
    return rlist

def set_ten():
    # media팀에서 원한 형식으로 맞추기 위한 함수
    keyword = get_key()                                                                                                             
    keyword_set = []
    
    # keyword 당 10개의 연관검색어 입력
    for i in keyword:
        
        a = Related(i)
        while len(a) <10 :
            a.append('null')
        
        keyword_set.append(a)
    # 연관검색어를 한개의 리스트에 쭉 나열
    related = []
    for i in keyword_set:
        for m in range(10):
            
            related.append(i[m])
    # 미디어팀이 원하는 형식으로 맞추기
    related_set = []
    for i,j in enumerate(related):
    
    
        #나머지 inde_1, 몫 inde
        inde_1 = i%10
        inde = i//10
    
        if inde_1==0:
            
            related_set.append([keyword[inde],j])
        
        else:
        
            related_set.append(['',j])
    
    return related_set


