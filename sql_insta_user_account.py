#from . import config
#from . import database

#from .database import sql
#from config import * 

from database.sql import selects
from database.sql import *
from collect.instagram_crawling import *
#print(selects('keywords'))
import json
import datetime
Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y-%m-%d')

#inserts('keywords', ('id','keyword'),[[1, '아이폰11' ],['2','갤럭시S20'],['3','QLED8K'],['4','비스포크'],['5','공기청정기']])
#commit()
#insert( 'keywords', { 'keyword': '핸드폰'})

# put_keyword 는 처음에만
#keyword = [['1', '아이폰11' ],['2','갤럭시S20'],['3','QLED8K'],['4','비스포크'],['5','공기청정기']]
#put_keyword(keyword)


# user_id 가져오기
def get_insta_userid():
    userid = set()
    try:
        rs = selects('search_records',('user_id'))
        for i in rs:
            userid.add(i[0])
    except:
        return 'select user_id failed'
    # 중복제거 안하는 이유는 update할 때 where문 쓰기 편함!
    return list(userid)


# 인기게시글 유저의 유저 정보.
def put_user_account(userid):
    #userid = ['a','b']
    #userid 는 단일 스트링값
    user_data = []
    user_data_1 = []
    k = 1
    for i in userid:
        try:
            inf = insta_famous_user(i)
            infor = inf[0]
            infor_1 = inf[1]
            # user_account_accu 에 넣기
            c = [infor['id'],infor['follower'],infor['following'],infor['post_num'],json.dumps(infor_1),DATE]
            # user_account update 하기
            d = (infor['id'],infor['follower'],infor['following'],infor['post_num'],json.dumps(infor_1),DATE,k)
            user_data.append(c)
            user_data_1.append(d+d)
            k+=1
        except:
            continue
    #print(search_data)
    
    # 이런 형식으로 넣어야 함
    # update search_records set feed_id = %s , user_id = %s, like = %s, cmt = %s,
    # type = %s, day = %s, content_info = %s, uploade_day = %s where id = %s and channel = %s
    # 
    try:
        inserts('user_account_accu',('user_id','follower','following','feed_total','user_info','day'),user_data)
        insert_update('user_account',['user_id','follower','following','feed_total','user_info','day','id'],user_data_1)
        commit()
        print('complete') 
    except:
        return 'user_account insert failed'

#keywords = selects('keywords')
#print(selects('keywords',['id','keyword']))




#updates test
#search_data_1 = [ ('abc', 'abc', json.dumps({}),'20200303','20200303','1','0'),('bbc', 'bbc', json.dumps({}),'20200303','20200303','2','0') ]
#updates('search_records',['id','keyword_id'],search_data_1,['feed_id', 'user_id', 'feed_info', 'day', 'upload_day'])
#commit()

'''
exec('SELECT * FROM search_records WHERE id = %s AND keyword_id= %s',(46,2))
json_results('*')
print(json_results(''))

insert_update('search_records',['id','keyword_id','feed_id','user_id','channel','is_popular','lik','cmt','day','upload_day'],[('46','1','a','a','b','1','1','1','20200101','20200101','46','1','a','a','b','1','1','1','20200101','20200101'),('47','1','a','a','b','1','1','1','20200101','20200101','47','1','a','a','b','1','1','1','20200101','20200101')])
commit()
#save_1('search_records',('id','keyword_id','feed_id','user_id','channel','is_popular','lik','cmt','day','upload_day'),('id','keyword_id'))

#exec('INSERT IGNORE socialDB.search_records (id,keyword_id, feed_id,user_id,channel,is_popular,lik,cmt,day,upload_day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE id=%s,keyword_id=%s',('46','2','a','a','b',1,'1','1','20200101','20200101',46,3))
#commit()

#print(selects('search_records','*','','',-1,id=46,keyword_id=1))

#INSERT IGNORE search_records (id,keyword_id, feed_id,user_id,channel,is_popular,lik,cmt,day,upload_day) VALUES ('46','1','a','a','b','1','1','20200101','20200101') ON DUPLICATE KEY UPDATE ('46','1','a','a','b','1','1','20200101','20200101')


#INSERT IGNORE socialDB.search_records ( feed_id,user_id,channel,is_popular,lik,cmt,day,upload_day) VALUES ('a','a','b',1,'1','1','20200101','20200101') ON DUPLICATE KEY UPDATE id=46,keyword_id=1


#delete('keywords','id')
#commit()

# DB 수정 a
#print(selects('search_records'))
'''
