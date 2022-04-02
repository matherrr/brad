from flask import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
import config
from database.sql import *
import json
from flask_cors import CORS, cross_origin
from database.sql import selects
from database.sql import *
from collect.instagram_crawling import *
import datetime
import re

# Default JSON encoder 는 set 을 JSON으로 변환할 수 없다.
# 커스텀 엔코더를 만들어 set을 list로 변환 후 JSON으로 변환하게 함
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return JSONEncoder.default(self, obj)


app = Flask(__name__)

CORS(app)  # CORS 해결해주는 구문

app.json_encorder = CustomJSONEncoder

def confirm(data,key,add_data):
    try:
        data[key].append(add_data)
    except:
        data[key]=[]
        data[key].append(add_data)
    return data

def add_key(data,key):
    try:
        type(data[key])
    except:
        data[key] = {}
    return data








'''
# 키워드 목록을 프론트로 쏴준다 return -> {keyword : [s10, qled8k, .....]}
@app.route('/chart', methods=['POST'])
def graph_2():
    data = request.get_json(force=True)
    DA = []
    for i in data['channel']:
        for j in data['keyword']:
            for k in data['day']:
                DA.append((i,j,k))
    print('2')
    print('1')

    return json.dumps(data,ensure_ascii=False)
'''

@app.route('/chart', methods=['POST'])
def graph_3():
    data = request.get_json(force=True)
    if len(data)==0:
        return json.dumps({},ensure_ascii=False)
    print(data)

    grahp_data = exec('''select keywords.keyword, search_records_accu.day, search_records_accu.post_num, search_records_accu.channel
                    from keywords left join search_records_accu 
                        on keywords.id = search_records_accu.keyword_id 
                            where channel=%s and keyword=%s and day=%s 
                            ''', data)  #날짜 기준으로 중복값 출력 제거
    result = results()
    #print(result)
    data = {}

    
    for ind,tpl in enumerate(result):
        data = add_key(data,tpl[3])
        add_data = {'total_cmt':tpl[2], 'day': str(tpl[1])[:10] }
        key = tpl[0]
        data[tpl[3]] = confirm(data[tpl[3]],key,add_data)

            
    return json.dumps(data,ensure_ascii=False)

'''
def exist_or_not(data,string):
    if data.find(string)!=-1:
        return data.find(string)
    else:
        return len(data)

def hash_select(data):
    data = data.replace('"','')
    tag = []
    while data.find('#')!=-1:
        c = data.find('#')
        #while a[0] == ' ': a = a[1:]
        short_data = data[c+1:]
        print(short_data)
        ind = min(exist_or_not(short_data,'\\'),exist_or_not(short_data,'#'),exist_or_not(short_data,' '))
        print(short_data[:ind])
        tag.append(short_data[:ind])
        data = data[c+ind:]
    return tag
'''


@app.route('/viewCards', methods=['POST','GET'])
def cards(): 
    grahp_data = exec('''select search_records_accu.channel, keywords.keyword, search_records_accu.day, json_extract(feed_info, '$.say'), json_extract(feed_info, '$.image') \
                            from keywords left join search_records_accu \
                                on keywords.id = search_records_accu.keyword_id \
                                ''', params=None)  #날짜 기준으로 중복값 출력 제거
    
   
    result = results()
    
    data = {}
    # image 와 say는 전처리가 필요
    
    for row in result :
        
        
        da = row[2].strftime('%Y-%m-%d')
        type(da)
        #_say = hash_select(row[3]) #전처리 필요
        regex = re.compile('#([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+|\w+)(\\\\|#|\s|)')
        A = regex.findall(row[3])
        _say = [i[0] for i in A]
        _url = row[4].replace('"','') #전처리 필요
        #print(_say)
        #print(_url)
        data = add_key(data,row[0])
        try:
            
            data[row[0]][row[1]].append({'say' : _say, 'url': _url, 'day': da})
            #data[row[0]][row[1]][row[2][:10]].append({'say' : row[2], 'url': row[3]})

        except:
            data[row[0]][row[1]] = []
            data[row[0]][row[1]].append({'say' : _say, 'url': _url, 'day': da})
            None # ing
        
    return json.dumps(data,ensure_ascii=False)

''' viewCards api constructure
# say : 태그 전처리 필요 / image : url / day : 수집 시점 / channel : insta

# day와 channel 특히 day를 키값으로 빼는게 좋을까??
    'channel' : {
        'keyword' : {
            'day': [
                    {'say' : ['#s10 s20'] , 'url' : 'www.~~~' },
                    {'say' : ['#s10 s20'] , 'url' : 'www.~~~' },
                    {'say' : ['#s10 s20'] , 'url' : 'www.~~~' }
                ]
            }
        }

    }

'''

if __name__ == '__main__':
    app.run(debug=True)



