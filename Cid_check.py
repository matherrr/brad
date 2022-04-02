#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:38:02 2019

@author: ptck
"""



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:44:22 2019

@author : ptck
"""
import csv
import sys, traceback, time
#from os import environ
#import time


#import os
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup

#from pandas import Series, read_csv

#from multiprocessing import Pool
from urllib import parse
#from functools import partial
import datetime
from os import makedirs
from os import chdir


#chdir('/Users/ptck/Downloads')
Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y/%m/%d/%H')


origin_input_path = './dbproj/includes/'
origin_output_path='./output/%s/'%(DATE)



try :
    makedirs(origin_output_path)
except:
    pass




#합쳐진 csv 파일 불러오기
    

def read_file(filename) :
    origin_input_path = './dbproj/includes/'
    # csv file 읽기 위함
    f = filename
    models = dict()
    with open(origin_input_path+f, 'r', newline='',encoding='euc-kr') as file:
        models['품목']=[]
        models['그룹']=[]
        models['키워드']=[]
        models['랜딩URL']=[]
        models['매체']=[]
        for num,line in enumerate(file.readlines()):
            # 0번째에는 품목명이니까 제외
            lines = line.split(',')
            # 0row에는 필요없는 정보
            if num <=0:
                continue
            # 품목이 빈 스트링일 경우 더이상 유알엘 없음
            if lines[0]=='':
                break
            
            # keyword 삽입
            models['품목'].append(lines[0])
            models['그룹'].append(lines[1])
            models['키워드'].append(lines[2])
            models['랜딩URL'].append(lines[3])
            models['매체'].append(lines[4])
            # 모델명만 가져오기 위함
            #try :
            #
            #    a = lines.index('')
            #    models['model'].append(lines[1:a])
            #except:
            #    models['model'].append(lines[1:])
                
            
    #print(csv_data)
    return models




#Table = read_csv(origin_input_path+'Keyword.csv',encoding='euc-kr',low_memory=False)
Table = read_file('Keyword.csv')

key = Table["품목"]
group = Table["그룹"]
keyword = Table["키워드"]
url = Table["랜딩URL"]
ngd = Table["매체"]

def Check_Unicode(keyword, url) :
    check_col = []
    te = []
      
    for i in range(len(url)):
        url_1 = url[i][::-1]

        cut_num = url_1.find("_")

        try :
            fin_num = url_1.find("#")
        except:
            fin_num = 0
        if cut_num <= fin_num:
            fin_num = 0 
        url_3 = url_1[fin_num:cut_num]
        url_final = url_3[::-1]
        text = parse.unquote(url_final) #url의 유니코드가 한글로 바뀐게 text
        text_upper = text.upper()
        te.append(text_upper)
        if keyword[i].upper()  == te[-1] :
            check_col.append("일치")
        else : 
            check_col.append("불일치")
    return check_col,te


def Concate_Table(keyword,url):
    check = Check_Unicode(keyword, url)

    return check 


"이 위는 URL cid 변환 정상 여부 체크"
"---------------------------------------------------------------"
"여기서부턴 URL 랜딩 정상 여부 체크"


def remove_dup(url):
    # dup_N 은 중복 url 갯수, short_url은 cid값을 다 제거한 url
    
    dup_N = []
    short_url = []
    url_1 = []
    for i in url:
        if '?' in i:
            
            num_1 = i.index('?')
        
            url_1.append(i[:num_1])
        else:
            url_1.append(i)
    #know_url.append(i[num_2+4:num_1])
    #N = list(set(know_url))
    a = 1

    for i,j in enumerate(url_1) :
        if i == len(url_1)-1:
            dup_N.append(a)
            short_url.append(j)
            break
        elif (i == 0) & (j != url_1[1]):
            dup_N.append(a)
            short_url.append(j)
            continue
        elif j == url_1[i+1]:
            a+=1
            continue
        
        else:
            dup_N.append(a)
            short_url.append(j)
            a = 1
            continue
  
    return short_url, dup_N


def Check_URL(k):      
    start_time = time.time()
    URL_list = k

    CheckList = []
    
    for url in URL_list :
        
        while True:
            try:
                url_data = requests.get(url, verify=False)
                
                url_check = url_data.status_code
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                time.sleep(5)
                continue
        if 200 <= url_check <300:
            CheckList.append("정상 랜딩중")
        
        elif 300 <= url_check <400 :
            CheckList.append("비정상 랜딩중 (리다이렉팅)")
        else:
            print(url)
            print(url_check)
            CheckList.append("비정상 랜딩중")
        
        '''
        if len(url_redirected) == 0:   # 리다이렉트 되지 않는 경우라면 url이 정상랜딩 혹은 랜딩이 안되는 경우 2가지있음
            
            if url_check == 200 :
                
                
                # if soup.find("div",{"class":'event-end-txt'}).find('strong').text != "이벤트가 종료되었습니다." :
               
                # 이렇게 바꿔야 하지 않을까?? 
                if soup.find("div",{"class":'event-end-txt'}) : 
                    if soup.find("div",{"class":'event-end-txt'}).find('strong').text != "이벤트가 종료되었습니다."  :
                        CheckList.append("비정상 랜딩중 (이벤트 종료)")
                        A.append("")
                
                # 200 에는 정상 랜딩 중과 이벤트 종료되었습니다 두 경우가 있음. 이벤트종료는 비정상 랜딩으로 구분해줘야함
                
                else : 
                    CheckList.append("정상 랜딩중")
                    A.append("")
                #else: # 200번이지만, 이벤트가 종류되었습니다 문구가 있는 경우는 비정상 랜딩으로
                #    CheckList.append("비정상 랜딩중 (이벤트 종료)")
                
            else :
                CheckList.append("URL 찾을 수 없음")  #200번호대는 정상이고 나머지는 리다이랙트 되는경우아니니까 url찾을 수 없음이 맞음 
                A.append(url_check)
        else: # 리다이렉트 되는 경우 이다. 
            num = len(url_redirected) - 1  # 리스트 0부터 세니까
            Last_redirected = url_redirected[num]  # 마지막으로 리다이렉트된 주소의 300 200 이런 값들이 나옴
            #print(Last_redirected)  # 이부분해봐야 뒷부분이 명확해질듯. 200,300 값나오는거면 바로 비교해도되고 아니면 url로 바꺼 비교해도되고
            if Last_redirected == 200 :
                CheckList.append("비정상 랜딩중 (리다이렉팅)")  ### 수정필요! 리다이렉트 되면 비정상으로 해야함. 그럼 그냥 redirected되면 다 비정상으로
                A.append(Last_redirected)
                #
                # 이부분이 수정요함. 리다이렉트로 정상랜딩이 되도 아예 다른 페이지가 뜰 수가 있다면 .. 그리고 이경우가 있다면 우리가 확인 할 방법이 없음.
                # 페이지를 하나하나 다 눈으로 확인해야하니까. 
                ### 아니면 리다이렉트되기전의 url에 박힌 상품 변환유니코드가 마지막 리다이렉트된 페이지 소스에 있다면 제대로 랜딩된거라 인식하게끔 로직을 짜던가
            else: 
                CheckList.append("비정상 랜딩중 (URL 찾을 수 없음)")
                A.append(Last_redirected)
                # 이 마지막 렌딩된 url페이지가 정상적으로 켜졌으나 과연 맞는 페이지인지 구분해야함
                # 만약 정상적으로만 떠도 다 정상이라고 체크한다고 치면, 리다이렉트 있을 경우도 그냥 2가지 경우로 마지막 리다이렉팅 랜딩페이지가 정상or 찾을수 없을으로 구분하면됨
            '''
    print("-------- %s seconds --------" % (time.time() - start_time))            
    return CheckList

def put_url_N(check, url_N):
    #short = []
    check_value = []
    
    for k,o in enumerate(check):
        i=0
        while i!=url_N[k]:
            check_value.append(o)
            #short.append(short_url[k])
            i+=1

    #Ch = DataFrame(check_value,columns=['URL_Check'])
    return check_value


print('Start')
short_url = remove_dup(url)[0]

Num_list = remove_dup(url)[1]

#result1은 cid값 확인값 list
result1 = Concate_Table(keyword,url)[0]

#result2는 url check한 값들 
Ch = Check_URL(short_url)
result2 = put_url_N(Ch,Num_list)




def MakeTable(key,group,keyword,url,ngd,cid,check):
    final = []
    name = ['품목','그룹','키워드','랜딩URL','매체','일치 여부','Status']
    a = len(key)
    final.append(name)
    for i in range(a):
        final_1 = []
        final_1+= key[i], group[i], keyword[i], url[i], ngd[i], cid[i], check[i]
        final.append(final_1)
    return final

Final = MakeTable(key,group,keyword,url,ngd,result1,result2)

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)



with open(origin_output_path+'Cid&URL_Check.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile,dialect='mydialect')
    for row in Final:
        thedatawriter.writerow(row)


'''    


url = 'https://www.samsung.com/sec/support/model/SL-C480W/'


url_data = requests.get(url, verify=False) #(url, allow_redirects = True)
#url_text = url_data.text
#soup = BeautifulSoup(url_text, 'html.parser')
url_redirected = url_data.history
url_check = url_data.status_code

'''
