from dbproj.db_data import landing as data
from dbproj.db_http import http
import traceback


def check_landings(limits=10) :
    for land in data.url.list_to_go(limits) :
        # 
        land.mark_visit()
        # TODO: multi-threading?
        try :
            resp = http._get_http(land.location)
            land.status_code = resp.status_code
            responsed = {
                'head': resp.headers,
                'url': resp.url,
                'body': resp.text,
            }
            # has redirect history
            info = land.info
            if resp.history is not None and 0<len(resp.history) :
                if info is None info = {}
                redirecteds = ['[%d] %s'%(r.status_code, r.url) for r in resp.history]
                info.update(redirect=redirecteds)
            # has error

            if 200 <= resp.status_code and reesp.status_code < 300 :
                land.mark_complete(resp.status_code, responsed, None, info)
            else :
                land.mark_complete(resp.status_code, None, responsed, info)
        except :
            land.mark_complete(None, None, traceback.extract_tb())

# 원격에서 내용 확인
def remote_validation(location:str, visited_at=None, collected_at=None, status:int=None, resp=None, info=None) :
    land = data.url.find_or_new_location(location)
    land.status_code = status if status is not None else 200
    land.response = resp
    land.errors = None
    # save remote check
    land.remote_visit(info, visited_at, collected_at)

''' Landing URL을 생성 또는 저장
@param interval: 수집 시간
    0 > interval - 삭제 (목록에도 포함 x)
    0 = interval - 수집 중단
    0 < interval - interval 시간(hours)마다 수집
@param retry: 에러 발생시 재확인 시간
    0 => retry - 재확인 안함
    0 < retry - retry 분(minute) 이후 발견되면 재수집

@return 저장된 수정 URL 주소
'''
def save_url(location:str, interval:int=24, retry:int=30) :
    land = data.url.find_or_new_location(location)
    land.interval = interval
    land.retry = retry

    return land.location

''' URL 목록 받아오기
@param after_id: id 커서, int SELECT 의 WHERE after_id < id)
@param per_a_page: 한 페이지 분량, int. SELECT의 LIMIT)
@param exclude_pause: True 일 경우 중지 (interval=0) 상태 URL 제외 (기본 포함)
@param include_delete: True 일 경우 삭제 (interval<0) 상태 URL 포함 (기본 제외)
'''
def urls(before_id:int=0, per_a_page:int=100, exclude_pause=False, include_delete=False) :
    return data.url.lists(before_id, per_a_page, exclude_pause, include_delete)


def campaigns(url_ids:tuple, **filters) :
    return data.campaign.search_campaigns(url_ids, **filters)

def save_campaign(url_id, campaigns) :
    rets = []
    for cdata in campaigns :
        c = data.campaign.build(target_id=url_id, **cdata)
        c.save()
        cv = c.values
        cv.update(id=c.id)
        rets.append(cv)
    return rets

def delete_campaigns(campaign_ids) :



