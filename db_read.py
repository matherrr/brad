
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
import nshop_common as db

#day = time.strftime('%Y%m%d', time.localtime(time.time())) # ex- 20191028
#hour = time.strftime('%H', time.localtime(time.time()))
filename = '/Users/ptck/Documents/repo_db-project/db-project/dbproj/Naver_0212.csv'

# csv파일을 읽어오는 함수
def read_file(filename):
    f = filename
    with open(f) as file:
        csv_data = []
        for line in file.readlines():
            # print(line)
            csv_data.append(line.split(','))  # .strip() 추가
    # print(type(csv_data)) = list type
    return csv_data


# csv에서 키워드을 뽑아오는 함수
def read_keyword():
    csv_data = read_file(filename)
    keyword_list = []
    for i in range(2, len(csv_data)):
        key = csv_data[i][1].strip()  # .replace('\xa0','')    #마지막에 .strip() 추가
        keyword_list.append(key)

    cut_num = keyword_list.index('')

    keyword_list = keyword_list[:cut_num]

    return keyword_list  # , cut_num


# csv파일에서 [모델명들......] 로 뽑아주는 함수
def read_items():
    csv_data = read_file(filename)
    cut_num_2 = len(read_keyword())
    raw_list = csv_data[2:cut_num_2 + 2]

    items_lst = []
    for lst in raw_list:

        try:
            lst_1 = lst[2:]  # 여기까진 다 통과하고 밑줄에서 에러나면 except문으로 넘어간다 # 모델명만 저장할꺼면 1->2로만 바꿔주면됨
            lst = []
            # csv파일 줄때 복붙을 해서 줬는지, 추가한 몇 데이터들에 \xa0가 생김. 처리해줄려고 만듬. DB에만 넣으면 고민해줄필요 없음
            for lls in lst_1:
                lls = lls.replace('\xa0', '')
                lst.append(lls)
            num_cut = lst.index('')
            items_lst.append(lst[:num_cut])
        except:
            lst = lst[:]  # 없어도 되는 줄
            lst[len(lst) - 1] = lst[len(lst) - 1].strip()  # .replace('\xa0','')  # TV마지막 모델명에 \n 지우기위해 추가함  # 임시방편임.
            items_lst.append(lst)
    return items_lst



# csv파일을 통해 키워드와 모델명들 딕셔너리 형태로 저장하는 함수
def dict_items():
    keyword_list = read_keyword()
    items_list = read_items()

    dict_product = {}
    for i in range(len(keyword_list)):
        dict_product[keyword_list[i]] = items_list[i]

    return dict_product


# 하나의 키워드에 대해 json이 만들어져야함
def model_json():
    
        
    md_json = json.dumps(json_form)
    return md_json



# 디비에 키워드를 적재하는 함수
@db.mysql_query('''insert into nshop_search_keywords(word) values (%s)''', with_transaction=True)
def put_keywords(cursor):

    data = []
    
    for keyword in read_keyword():
        data.append([keyword])    
    #append(keyword)오류남. ([keyword])로 어팬드해야..
    return data


# 디비에 모델명을 적재하는 함수 json형식으로
@db.mysql_query('''insert into nshop_search_keywords(models) values (%s)''', with_transaction=True)
def put_models(cursor):
    

    return data



# 실행단에서는 처음 csv파일을 처음 받았을때, csv파일의 키워드와 모델명을 디비에 저장하는 기능을 한다.
if __name__ == '__main__':
    with db.mysql_connection() as cursor:

        put_keywords(cursor)
        #put_json(cursor) -> json 파일보다는 그냥 리스트로 해당 모델명 넣어버리는게 좋을듯
