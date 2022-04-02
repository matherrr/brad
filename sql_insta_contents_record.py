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
        print('select user_id failed')
    # 중복제거 안하는 이유는 update할 때 where문 쓰기 편함!
    return list(userid)



# keyword 당 인기 게시물은 9씩을 가져올 수 있음.
def put_content_records(k,userid):
    
    #userid 는 단일 스트링값
    content_data = []
    content_data_1 = []
    try:
        infor = insta_user_post_information(userid)
        #print(infor)
    except:
        
        return 'insta_user_post_information failed'
    for j,i in enumerate(infor):
        try:
            # content_records_accu 에 넣기
            c = [i['unique'],'instagram',i['user_id'],i['like'],i['comment'],i['type'],DATE,i['content_info'],i['time']]
            #print(1)
            # content_records에 update 하기
            d = (i['unique'],i['user_id'], i['like'],i['comment'], i['type'], DATE, json.dumps(i['content_info']), i['time'], k, 'instagram' )
            #print(2)
            k+=1
            content_data.append(c)
            #print(3)
            content_data_1.append(d+d)
            #print(4)
        except:
            print('error')
            continue
    #print(search_data)
    print(j)
    # 이런 형식으로 넣어야 함
    # update search_records set feed_id = %s , user_id = %s, like = %s, cmt = %s,
    # type = %s, day = %s, content_info = %s, uploade_day = %s where id = %s and channel = %s
    # 
    try:

        inserts('content_records_accu',('feed_id','channel','user_id','lik','cmt','type','day','content_info','upload_day'),content_data)
        insert_update('content_records',['feed_id', 'user_id', 'lik', 'cmt', 'type', 'day','content_info', 'upload_day','id','channel'],content_data_1)
        commit()
        print('complete') 
    except:
        return 'content_records insert failed'    

#keywords = selects('keywords')
#print(selects('keywords',['id','keyword']))

# userid 받아서 모두 넣기
def put_content_records_all(k,userid):
    
    for i in userid:
        try:
            put_content_records(k,i)
            k+=12
        except:
            continue

#put_content_records_all(1,get_insta_userid())

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
