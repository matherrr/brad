from .chrome_driver import insta
import datetime
import traceback
Da_1 = datetime.datetime.now()
DATE = Da_1.strftime('%Y-%m-%d')



#driver만 가져오기
'''
def driver_excute(chromedriver_location='/Users/ptck/Downloads/chromedriver'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver_location, chrome_options=options)
    return driver

# js코드로 정보 가져오기
def driver_excute_one(url,key,comment,chromedriver_location='/Users/ptck/Downloads/chromedriver'):
        driver = driver_excute(chromedriver_location)
        driver.get(url+'/'+key+'/')
        js = "return "+comment
        all = driver.execute_script(js)
        driver.quit()
        return all
'''
# video_photo_rate = 비디오 게시물 / 전체 게시물 

key_mapping ={
    'username' : 'id',
    'full_name' : 'name',
    'biography' : 'biography',
    'edge_owner_to_timeline_media' : 'post',
    'edge_follow' : 'follower',
    'edge_followed_by' : 'following',
    'edge_felix_video_timeline' : 'video_photo_rate'
    
}

ins = insta()

##############키워드 검색시, 인기 게시물 정보 따따따 부셔버려 따따따
def insta_crawling_keyword(keyword):
    return ins.js_excute('https://www.instagram.com/explore/tags',keyword,'__initialData.data.entry_data.TagPage[0].graphql.hashtag')

### @yg user profile 무시함?
def insta_crawling_profile(user_id) :
    return ins.js_excute('https://www.instagram.com',user_id,'__initialData.data.entry_data.ProfilePage[0].graphql.user')

### @yg 


# @yg HTTP Request 는 최소한으로
# rs = insta_crawling_keyword(keyword)

def confirm_keys(data,key:list,default=''):
    try:
        for ki,ky in enumerate(key):
            data = data[ky]
        return data
    except :
        return default


#게시물 갯수
def insta_keyword_post(rs):
    
    return confirm_keys(rs,['edge_hashtag_to_media','count'])
    
#관련 해시태그
def insta_keyword_hash(rs):
    Tag= []
    tag = confirm_keys(rs,['edge_hashtag_to_related_tags','edges'])
    for i in tag:
        Tag.append(confirm_keys(i,['node','name']))
    return Tag
    
# ful = insta_famous_post(rs)
def insta_find_id(unique):
    infor = ins.js_excute('https://www.instagram.com/p',unique,'__initialData.data.entry_data.PostPage[0].graphql.shortcode_media.owner')         
    return confirm_keys(infor,['username'])

#인기게시물 or 최신게시물고유문서문자 및 좋아요, 댓글 수
def insta_post(rs,top):
    # top : 'edge_hashtag_to_media' or 'edge_hashtag_to_top_posts'
    # sum = [ {'unique': dsklfjl, 'like': 21, 'comment':53},{...},{...}]
    ful = []
    # 고유문서문자
    # ful['unique']=[]
    # # 좋아요수
    # ful['like']=[]
    # # 댓글수
    # ful['post']=[]
    form = '%Y-%m-%d'
    famous_data = confirm_keys(rs,[top,'edges'])
    if famous_data !='':

        for i,j in enumerate(famous_data):
            node = confirm_keys(j,['node'])
            T = confirm_keys(node,['taken_at_timestamp'])
            t = datetime.datetime.fromtimestamp(float(T)) if T !='' else 0
            # @yg 심플리
            ful.append({
                'user_id': insta_find_id(node['shortcode']),
                'unique': confirm_keys(node,['shortcode']),
                #'unique': node['shortcode'],
                'like': confirm_keys(node,['edge_liked_by','count']),
                #'like': node['edge_liked_by']['count'],
                'comment': confirm_keys(node,['edge_media_to_comment','count']),
                #'comment': node['edge_media_to_comment']['count'],
                'image':confirm_keys(node,['display_url']),
                #'image': node['display_url'],
                'say' : confirm_keys(node,['edge_media_to_caption','edges',0,'node','text']),
                #'say' : node['edge_media_to_caption']['edges'][0]['node']['text'],
                'time': t.strftime(form),
            })

        # ful[i]['unique']=j['node']['shortcode']
        # ful[i]['like']=j['node']['edge_liked_by']['count']
        # ful[i]['comment']=j['node']['edge_media_to_comment']['count']
    return ful

    
########## 사용자 검색


# @yg chromedriver_location 은 이 파일에서 완전히 신경 안 쓰도록 합시다
# ui = insta_crawling_profile(user_id)
def insta_find_user(user_id):
    # user_id 는  스트링 형태로 삽입
    # Val = [ {'id': dsklfjl, 'name': 이동우, 'biography':나는 산다, 'post': 60, 'follower':430, 'following': 30,'video_photo_rate':0.1},{...},{...}]
    Val = {}

    # infor = ins.js_excute('https://www.instagram.com',user_id,'__initialData.data.entry_data.ProfilePage[0].graphql.user')
    # @yg 심플 & 심플러. 근데 ins 계속 달고 다녀야 함? 이거 chromedriver 인스턴스 아냐?
    try:
        infor = insta_crawling_profile(user_id)
    except:
        return 'profile failed'
    outlier = ['edge_owner_to_timeline_media','edge_follow','edge_followed_by','edge_felix_video_timeline']
    for j in infor:
        
        if j in list(key_mapping):
            
            if j in outlier:
                Val[key_mapping[j]] = confirm_keys(infor[j],['count'])
                continue
            else:
                Val[key_mapping[j]] = infor[j]
    Val['video_photo_rate'] = Val['video_photo_rate']/Val['post']

    
    return Val,infor



def insta_famous_user(userid):
    try:
        al = insta_find_user(userid)
    except:
        return 'find_user failed'
    ful = al[0]
    exe = al[1]
    # id 와 name을 가져오는 작업
    ful['profile_image'] = confirm_keys(exe,['profile_pic_url'])
    ful['post_num'] = confirm_keys(exe,['edge_owner_to_timeline_media','count'])
    return ful,exe




'''
# 고유문서문자로 유저 아이디, 게시물수, 팔로워, 팔로잉 숫자 
# rs = insta_crawling_keyword(keyword)
def insta_famous_user(rs):
    
    Val = []
    
    # input은 insta_famous_post의 출력값을 모두 받지만, 사용하는 건 ful[i]['unique']만
    # @yg insta_famous_post 에 집어 넣을 결과 값 가져와야겠네요
    
    ful = insta_famous_post(rs)
    # id 와 name을 가져오는 작업
    
    for i,j in enumerate(ful):
        Val.append({})
        # @yg 요것도 어떻게 줄여 볼 방법 없을까?
        #infor = ins.js_excute('https://www.instagram.com/p',j['unique'],'__initialData.data.entry_data.PostPage[0].graphql.shortcode_media.owner')
        insta_find_id(j['unique'])
        Val[i]['id']=insta_find_id(j['unique'])
    # insta_find_user 함수를 통해서 모든 정보 같이 넣기    
    for i,j in enumerate(Val):
        # @yg 얘들도.
        AA = insta_find_user(ins,j['id'])[0]
        for m in AA:
            if m in list(key_mapping):
                j[m] = AA[m]
        
    return Val
'''

# user id의 열두개의 게시물정보(해쉬태그 포함한 글 내용)를 가져오는 작업
# rs = insta_crawling_profile(user_id)
def insta_user_post_information(user_id):
    # 여기서 user_id 는 스트링 한개로!
    # post_12 = { 'id' : kasjdlkasjd, 'comment': 231231,21312312,12312312,123123,123123...}
    try:
        rs = insta_crawling_profile(user_id)
    except:
        return 'profile failed'
    post_12 = []
    #post = ins.js_excute(ins,'https://www.instagram.com',user_id,'__initialData.data.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.edges')
    
    form = '%Y-%m-%d'
    post = confirm_keys(rs,['edge_owner_to_timeline_media','edges'])
    if post != '':
        for i in post:
            node = confirm_keys(i,['node'])
            T = confirm_keys(node,['taken_at_timestamp'])
            t = datetime.datetime.fromtimestamp(float(T)) if T !='' else 0
            post_12.append({
                'user_id': user_id,
                'say' : confirm_keys(node,[ 'edge_media_to_caption','edges',0,'node','text']),
                'comment': confirm_keys(node,['edge_media_to_comment','count']),
                #'comment' : node['edge_media_to_caption']['edges'][0]['node']['text'] if node['edge_media_to_caption']['edges'][0] else '',
                'like' : confirm_keys(node,['edge_liked_by','count']),
                #'like' : node['edge_liked_by']['count'],
                'unique' : confirm_keys(node,['shortcode']),
                #'unique' : node['shortcode'],
                'type' : 'video' if node['is_video'] else 'image',
                'day' :  DATE,
                'time' : t.strftime(form),
                'content_info' : i
            })
    return post_12

