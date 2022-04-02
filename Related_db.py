# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:07:36 2019

@author: ptck
"""
import requests
import warnings
import time
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from urllib import parse
import mysql.connector
from mysql.connector import Error
import datetime
import json
import csv

#os.chdir('/Users/ptck/Downloads/')
Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y/%m/%d/%H')

origin_input_path='./dbproj/includes/'
origin_output_path='./output/%s/'%(DATE)

try:

    os.makedirs(origin_output_path)
except:
    pass

def related(key):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    key_list = key
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={}'.format(key_list)
    verify=False
    res = requests.get(url, headers=headers, verify=verify)
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

def related_search_1(keyword):
    bucket=[]
    
    
    for i in keyword:
        bucket.append(related(i))
    
        
    return bucket

def get_itmes_list():

    # db에서 인풋 가져오기
    cnx = mysql.connector.connect(user='root',password='pengtai123', 
        database='db-project')
    #conn = mysql.connector.connect(**mysql_conf)

    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()


    sql = "SELECT id, word FROM nsearchs ORDER BY id"
    curs.execute(sql)
    a = []
    for i in curs:
        
        a.append(i[1])
    
    cnx.close()
    #rows = curs.fetchall()
    b ={}
    b['aaa'] = ['1','2','3']
    return b

L = get_itmes_list()

def read_file(filename) :
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

#df = related_search_1(read_file('keyword_0819.csv'))

df = related_search_1(get_itmes_list())

def find_related(df,csv):
    
    keyword = get_itmes_list()                                                                                                             
    for i in range(len(df)):
        
        while len(df[i])<10:
            df[i].append('null')

    r_li=[]
    for i in range(len(df)):
        for j in range(10):
            r_li.append(df[i][j])
        
    R_li = []
    for i in range(len(r_li)):
    
    
        #나머지 inde_1, 몫 inde
        inde_1 = i%10
        inde = i//10

        if inde_1==0:
        
            R_li.append([keyword[inde],r_li[i]])
        
        else:
        
            R_li.append(['',r_li[i]])
    
    return R_li
  
    
    
df_2=find_related(df,get_itmes_list())


'''
def li_to_dic(key,li):
    st = []
    for i,j in enumerate(li):
        dic = {}
        dic["{}".format(key[i])]=j
        
        st.append( json.dumps(dic,ensure_ascii=False))
        
    return st
        
M = li_to_dic(get_itmes_list(),df)


M_1 = json.dumps(M,ensure_ascii=False)
'''







def into_db(key,li):
    
    cnx = mysql.connector.connect(user='root',     
        database='db-project',unix_socket='/var/run/mysqld/mysqld.sock')

    ## host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
    curs = cnx.cursor()
    
     
    
    Da_1 = datetime.datetime.now()
    DATE = Da_1.strftime('%Y%m%d%H')
    data_1 = []
    data_2 = {}  
    DA = []
    for i,j in enumerate(key):
        data_2['{}'.format(j)]=json.dumps(li[i],ensure_ascii=False)
        c = data_2['{}'.format(j)]
        #c_1 = data_2['{}'.format(j)]
        a = ('{}'.format(j),c,DATE)
        #a_1 = ('{}'.format(j),c_1)
        data_1.append(a)
        #DA.append(DATE)
    data_1=tuple(data_1)
    DA = tuple(DA)
    sql = """update nsearchs set resp = %s , updated_by = %s where word = %s """
    #sql_1 = """update nsearchs set word = %s where updated_by = %s"""
    curs.executemany(sql, data_1)
    #curs.executemany(sql_1, DA)
    cnx.commit()
    cnx.close()
    
# created_by -> 어떤 유저에 의해 생성되었는지

# nsearch_records에 결과값 추가하기
    cnx = mysql.connector.connect(user='root',     
        database='db-project',unix_socket='/var/run/mysqld/mysqld.sock')
    curs = cnx.cursor()
    data_3 = []
    data_2 = {}
    for i,j in enumerate(key):
        data_2['{}'.format(j)]=json.dumps(li[i],ensure_ascii=False)
        a = j
        b = data_2['{}'.format(j)]   
        c = (i+1,i+1,DATE,12,a,b)
        data_3.append(c)
    data_3 = tuple(data_3)

    sql = """insert into nsearch_records(id,word_id,date,hour,nsearch_recordscol,nsearch_recordsjson)
         values (%s, %s, %s, %s, %s, %s)"""
         
    curs.executemany(sql, data_3)
    cnx.commit()
    
    
    cnx.close()
    return



into_db(get_itmes_list(),df)

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)



with open(origin_output_path+'Naver_keyword_output.csv', 'w', newline='',encoding='euc-kr') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile,dialect='mydialect')
    for row in df_2:
        thedatawriter.writerow(row)












'''
df_2=find_related(df,'keyword_0819.csv')
#df_2_1=find_related(df,'keyword_0819.csv')[1]
df_3 = DataFrame (df_2, columns = [ 'Keyword','Related Keyword'])
df_3.to_csv(origin_output_path+'Naver_keyword_output.csv', sep=',', encoding='euc-kr', index=False)
'''
