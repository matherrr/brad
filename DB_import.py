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


# josn 파일 db정보 읽어오는 함수
def _config(filepath='/home/ubuntu/db-project/dbproj/database.config.json') :
#def _config(filepath='/home/ubuntu/db-project/dbproj/database.config.json'):
    conf = None
    with open(filepath, 'r', encoding='utf-8') as fp :
        conf = json.load(fp)
    return conf

# 데코레이션 함수
def with_connection(fn) :
    mysql_conf = _config(filepath='/home/ubuntu/db-project/dbproj/database.config.json')
    # mysql_conf = _config(filepath='/home/ubuntu/db-project/dbproj/database.config.json')
    conn = mysql.connector.connect(**mysql_conf,
                                   charset='utf8mb4')
    curs = conn.cursor()

    # 여기서 실행
    # 하위 함수 파라미터는 (cursor, connection) 순
    # connection을 전달하는 이유: 필요하면 connection.commit() 불러야 하니까
    result = fn(curs, conn)
    conn.close()
    return result

#  DB를 통해 nshop_seraches 테이블의 id 값과 키워드 값을 출력해줌
@with_connection
def get_keywords_list_DC(cursor, connection) :
    sql = '''SELECT id, word FROM nshop_searches order by id'''
    cursor.execute(sql)

    # 원본에 가깝게
    ids = []
    words = []
    for (_id, word) in cursor :
        ids.append(_id)
        words.append(word)

    return (ids, words)


# get_keywords_list_2() -> 이렇게 받으면 불러오는게 안됨. 오류남. 뒤에 () 없이 해야 불러와지네...;

@with_connection
def get_models_DC(cursor, connection):
    # SQL escaping은 "반드시" parameterizing 사용할 것.
    sql = '''SELECT id, name FROM nshop_search_models WHERE category=%s '''

    data_lst = []

    (ids, words) = get_keywords_list_DC
    for w in words:
        cursor.execute(sql, (w,))
        data = [n for (w, n) in cursor]
        data_lst.append(data)

    return data_lst


# 모델명을 딕셔너리로 불러오는 함수
@with_connection
def get_models_DCdic(cursor, connection):
    # SQL escaping은 "반드시" parameterizing 사용할 것.
    sql = '''SELECT id, name FROM nshop_search_models WHERE category=%s '''

    data_lst = dict()

    (ids, words) = get_keywords_list_DC
    for w in words:
        cursor.execute(sql, (w,))
        data_lst[w] = [n for (w, n) in cursor]

    return data_lst

#  count_num = '''selct count(*) from nshop_search_records''' 함수로 하나 뺄까?
# 참조테이블에 차곡 차곡 쌓기 위해서 현 참조테이블 데이터가 담긴 테이블의 개수를 알아옴. 그밑으로 저장하게 하려고
@with_connection
def get_num(cursor, connection):
    sql = '''select id from nshop_search_records order by id desc limit 1'''
    cursor.execute(sql)

    number = []

    for num in cursor:
        number.append(num)

    return number[0][0]


# 디비의 참조테이블에서 매칭에 필요한 데이터들만 불러오는 함수
@with_connection
def get_refTable_DC(cursor, connection):
    # SQL escaping은 "반드시" parameterizing 사용할 것.
    DAY = time.strftime('%Y%m%d', time.localtime(time.time()))

    #sql = '''SELECT word, item_name, item_rank, item_review, low_price, day, hour FROM nshop_search_records left join nshop_searches on nshop_search_records.word_id = nshop_searches.id where day='20191125' and hour='15' and word=%s; '''
    sql = '''SELECT word, item_name, item_rank, item_review, low_price, day, hour FROM nshop_search_records left join nshop_searches on nshop_search_records.word_id = nshop_searches.id where day=DAY and hour='10' and word=%s; '''

    Ref_data = {}
    (ids, words) = get_keywords_list_DC
    for w in words:
        Ref_data[w] = []
        cursor.execute(sql, (w,))
        #cursor.execute(sql, (d,w,)) day 수정할시
        read_lines = cursor.fetchall()
        #print(read_lines)

        for row in read_lines:
            Ref_data[w].append(row[1:])


    return Ref_data

k_list = get_refTable_DC['TV']


'''
# 잠시 주석처리
# 만드는 중입니다......완성됨
@with_connection
def get_adTable_DC(cursor, connection):
    # SQL escaping은 "반드시" parameterizing 사용할 것.
    DAY = time.strftime('%Y%m%d', time.localtime(time.time()))

    # 시간은 고정해둠. 나중에 변경해야할수도 있음
    sql = SELECT category, ad_item, ad_review, day, hour FROM nshop_search_records_ads where day='20191126' and hour='16' and category=%s; 

    Ref_data = {}
    (ids, words) = get_keywords_list_DC
    for w in words:
        Ref_data[w] = []
        cursor.execute(sql, (w,))
        #cursor.execute(sql, (d,w,)) day 수정할시
        read_lines = cursor.fetchall()
        #print(read_lines)

        for row in read_lines:
            Ref_data[w].append(row[1:3])


    return Ref_data

# 잠시 휴식
# 디비에서 광고순위 보고서 폼에 맞추어 뽑아오는 함수
@with_connection
def get_adTable(cursor, connection): ##
    # SQL escaping은 "반드시" parameterizing 사용할 것.
    DAY = time.strftime('%Y%m%d', time.localtime(time.time()))
    keywords = get_keywords_list_DC[1]

    total_data = []
    # 시간은 고정해둠. 나중에 변경해야할수도 있음
    sql = SELECT category, ad_item, ad_review, day, hour FROM nshop_search_records_ads where day='20191126' and hour='16' and category=%s; 
    for keyword in keywords :
        model_name_data=[keyword,'제품명']
        review_data=[keyword,'리뷰수']

        cursor.execute(sql, (keyword,))### 이줄 수정중
        #cursor.execute(sql, (d,w,)) day 수정할시
        read_lines = cursor.fetchall()
        for line in read_lines:
            model_name_data.append(line[1])
            review_data.append(line[2])

        total_data.append(model_name_data)
        total_data.append(review_data)

    return total_data






#decorator 디자인 패턴의 일반적인 구조 >
def decorator(fn) :
    def _decorator_wrapper() :
        # pre_process ...

        result = fn()

        # post_process ...
        return result

    # 새로 만든 함수를 반환한다
    return _decorator_wrapper 

@decorator
def decorator_target() :
    # 함수 내용
    pass 


#with_connection 은 입력으로 받은 함수의 실행 결과를 반환하기 때문에
#python 해석기의 입장에서 이렇게 실행됨 (위에서부터 순서대로)

# type(get_keywords_list_DC) == Function
def get_keywords_list_DC(cursor, connection) :
    함수 내용
    return (id, word)

# type(get_keywords_list_DC) == tuple << with_connection 의 반환값
get_keywords_list_DC = with_connection(get_keywords_list_DC)


#SQL 의 JOIN을 적극적으로 활용:

    sql = """SELECT id, category, name 
                FROM nshop_search_models m
                    JOIN nshop_searches w ON m.category = w.word
                WHERE w.word in (...)"""
    stmt = sql%(','.join(words))
    cursor.execute(sql)

    models = dict()
    for _id,word,model in cursor :
        if word not in models :
            models[word] = []
        models[word].append(model)
'''