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

#def put_keyword(keyword:list=[[],[]]):
#    try:
#        inserts('keywords',('id','keyword'),keyword)
#        commit()
#    except:
#        return 'insert keyword failed'


# put_keyword 는 처음에만
#keyword = [['1', '아이폰11' ],['2','갤럭시S20'],['3','QLED8K'],['4','비스포크'],['5','공기청정기']]
#put_keyword(keyword)

# keyword 가져오기
def get_insta_keyword():
    try:
        keyword = selects('keywords',('id','keyword'))
    except:
        return 'select keyword failed'
    return keyword

# keyword 당 인기 게시물은 9씩을 가져올 수 있음.


# keyword 당 인기 게시물은 9씩을 가져올 수 있음.
def put_search_records(k,index,keyword):
    
    search_data = []
    search_data_1 = []
    try:
        rs = insta_crawling_keyword(keyword)
        tag = insta_keyword_hash(rs)
        post_num = insta_keyword_post(rs)
        infor = insta_post(rs,'edge_hashtag_to_top_posts')
    except:
        return 'insta information failed'
    for j,i in enumerate(infor):
        try:
            i.update({'tag':tag,'post_num':post_num})
            # search_records_accu 에 넣기
            c = [i['unique'],i['user_id'],index,'instagram',post_num,i['like'],i['comment'],i,DATE,i['time']]
            # search_records에 update 하기
            d = (i['unique'],i['user_id'],'instagram',post_num,i['like'],i['comment'],json.dumps(i), DATE, i['time'], k, index )
            k+=1
            search_data.append(c)
            search_data_1.append(d+d)
        except:
            print('error')
            continue
    #print(search_data)
    print(j)
    # 이런 형식으로 넣어야 함
    # update search_records set feed_id = %s , user_id = %s, feed_info = %s, day = %s, upload_day = %s where id = %s and keyword_id=%s
    #
    try:
        inserts('search_records_accu',('feed_id','user_id','keyword_id','channel','post_num','lik','cmt','feed_info','day','upload_day'),search_data)
        insert_update('search_records',['feed_id', 'user_id','channel','post_num','lik','cmt','feed_info', 'day', 'upload_day','id','keyword_id'],search_data_1)
        commit()
        print('complete')  

    except:
        return 'search_records insert failed'

#keywords = selects('keywords')
#print(selects('keywords',['id','keyword']))

def put_general_records(k,index,keyword):
    
    search_data = []
    search_data_1 = []
    try:
        rs = insta_crawling_keyword(keyword)
        tag = insta_keyword_hash(rs)
        post_num = insta_keyword_post(rs)
        infor = insta_post(rs,'edge_hashtag_to_media')
    except:
        return 'insta information failed'
    for j,i in enumerate(infor):
        try:
            i.update({'tag':tag,'post_num':post_num})
            # search_records_accu 에 넣기
            c = [i['unique'],i['user_id'],index,'instagram',post_num,i['like'],i['comment'],i,DATE,i['time']]
            # search_records에 update 하기
            d = (i['unique'],i['user_id'],'instagram',post_num,i['like'],i['comment'],json.dumps(i), DATE, i['time'], k, index )
            k+=1
            search_data.append(c)
            search_data_1.append(d+d)
        except:
            print('error')
            continue
    #print(search_data)
    print(j)
    # 이런 형식으로 넣어야 함
    # update search_records set feed_id = %s , user_id = %s, feed_info = %s, day = %s, upload_day = %s where id = %s and keyword_id=%s
    #
    try:
        inserts('general_records_accu',('feed_id','user_id','keyword_id','channel','post_num','lik','cmt','feed_info','day','upload_day'),search_data)
        #insert_update('general_records',['feed_id', 'user_id','channel','post_num','lik','cmt','feed_info', 'day', 'upload_day','id','keyword_id'],search_data_1)
        commit()
        print('complete')
    except:
        return 'search_records insert failed'

def get_keyword(A):
    index = A['id']
    key = A['keyword']
    return index,key


# keyword 와 id 받아서 모두 넣기
def put_search_records_all(k,keyword):
    
    for i in keyword:
        try:
            
            put_search_records(k,get_keyword(i)[0],get_keyword(i)[1])
            k+=9
            
        except:
            continue

def put_general_records_all(k,keyword):
    
    for i in keyword:
        try:
            
            put_general_records(k,get_keyword(i)[0],get_keyword(i)[1])
            k+=72
            
        except:
            continue




#updates test
#search_data_1 = [ ('abc', 'abc', json.dumps({}),'20200303','20200303','1','0'),('bbc', 'bbc', json.dumps({}),'20200303','20200303','2','0') ]
#updates('search_records',['id','keyword_id'],search_data_1,['feed_id', 'user_id', 'feed_info', 'day', 'upload_day'])
#commit()
