
# crontab으로 돌려야 하는 파일.
# 1000개씩 키워드 별 오가닉 데이터를 크롤링하여 DB에 축적하는 파일

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

import db_common as DB
# DB_import 모듈을 사용하여 DB에 저장된 키워들 불러와 참조테이블을 만드는 파일

# 1. 키워드별 크롤링 함수  2. 크롤링한 자료 디비에 적재하는 함수

# 기존과 수정된 부분
# 1. 오가닉과 광고 순위 모두 크롤링해온다. -> is_organic 컬럼으로 구분하여 광고순위,오가닉순위를 판별
# 기존에는 오가닉만 크롤링하고, 광고순위는 1~2페이지만 따로 크롤링하여 처리하였지만, 하나의 테이블로 한번에 크롤링하는게 목적 


# 각 키워드 별 1000개정도 크롤링 해오는 함수(판다스없음)
def ref_Table(k):
    keyword = []
    model = []
    rank_id = []
    is_organic = []
    reviews = []
    is_price = []

    for a in range(1, 30):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        url = 'https://search.shopping.naver.com/search/all.nhn?origQuery={}&pagingIndex={}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={}'.format(
            k, a, k)

        res = requests.get(url, headers=headers, verify=False)
        text = res.text
        soup = BeautifulSoup(text, 'html.parser')

        lis = soup.find_all("li", {"class": "_itemSection"})
        # lst*B 광고 / lst*H 최저가없음 lst*C 최저가있는거 lst*N 이벤트
        # 이중 광고와 오가닉인 B, C, N 을 크롤링 해온다
        
        for li in lis:
            L = li.get("data-expose-area")
            R = li.get("data-expose-rank")
            if not L in ['lst*H']:

                if L in ['lst*B']: # 만약 광고라면
                    is_organic.append(0)   # 0 : false

                if L in ['lst*C']:
                    is_price.append(1)     # 1 : True 최저가있음을 뜻함
                    is_organic.append(1)   #
                else:                  # lst*N 일때
                    is_price.append(0)
                    is_organic.append(1)

                tit = li.find("div", {"class": "tit"})
                tit = tit.find('a')
                #print(tit)
                if tit is None:
                    continue
                text = tit.text.strip()
                #text = tit.text.replace(' ', '').upper() 일단 참조테이블에는 품목명 그대로 긁어와 저장시키기
                model.append(text)

                info = li.find("div", {"class": "info"})
                etc = info.find("span", {"class": "etc"})
                em = etc.find("em").text # em은 str
                em = em.replace(',','')  # 1,309 -> 는 int로 인식안함 (테이블 컬럼 타입이 int임)
                reviews.append(em if 0 < len(em) else 0)
                rank_id.append(R) # 한번에 처리하면 될듯
                keyword.append(k)

    return keyword, model, rank_id, is_organic, reviews, is_price
    # rank_id 에서 광고의 경우는 페이지 넘어갈때마다 리셋되므로 중복 존재



# 참조 테이블 크롤링하여 디비에 적재하는 함수
def put_Ref_Table():

    mysql_conf = DB._config(filepath='/Users/ptck/Damon_project/db-project/dbproj/database.config.json')
    conn = mysql.connector.connect(**mysql_conf)
    curs = conn.cursor()

    sql = '''INSERT INTO nshop_search_records (keyword, model, rank_id, is_organic,reviews, is_price)
    VALUES(%s, %s, %s, %s, %s, %s)'''

    for i in DB.get_nkey_func(cnx, cursor):   #i로 TV가 하나 들어가면
        data =[]
        raw_data = ref_Table(i) #키워드 하나에 대한 크롤링이 시작됨
        for j in range(len(raw_data[0])): # j는 오가닉아이템 긁어온 1000개만큼 돌리는거임

            keyword = raw_data[0][j]
            model = raw_data[1][j]
            rank_id = raw_data[2][j]
            is_organic = raw_data[3][j]
            reviews = raw_data[4][j]
            #print(reviews)
            is_price = raw_data[5][j]
            data.append([keyword, model, rank_id, is_organic, reviews, is_price])

        curs.executemany(sql, data)  #
        conn.commit()                #
        data.clear()                 #
        print("진행중..."+i+"완료...")

    conn.close()
    return None


if __name__ == '__main__':
    with DB.mysql_connection() as cursor:
        cnx= cursor[0]
        cursor = cursor[1]
        put_Ref_Table()