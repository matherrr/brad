#! -*- coding: utf8 -*-

import sys
import json
import traceback
import time

from datetime import datetime, timedelta

from dbproj.collector import timelog, chrome_worker, requests_worker
from dbproj.models import account
from dbproj.models import campaign
from dbproj.models import record

class browser(requests_worker) :
    def __init__(self, mode_debug=False) :
        super().__init__('naver', mode_debug)
    
    def set_account(self, login, access) :
        super().set_account(login, access)

        self.__common_args__ = {
            'account_id': self.account_id,
            'ad_channel': 'naver',
            'ad_type': 'search'
        }

        if self.api_info is not None :
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-API-KEY': self.api_info['api_key'],
                'X-Customer': self.api_info['customer_id'],
            }
            self.session.headers.update(**headers)

    def _signature(self, path, method='POST') :
        import hmac, hashlib, base64
        timestamp = int(datetime.now().timestamp())
        signature = hmac.new(
            bytes(self.api_info['secret'], encoding='utf-8'), 
            bytes('%d.%s.%s'%(timestamp, method, path), encoding='utf-8'),
            hashlib.sha256)
        signature.hexdigest()

        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Signature': base64.b64encode(signature.digest()),
            'X-Timestamp': '%d'%(timestamp),
        }

    def call(self, path, **params)  :
        self.session.headers.update(**self._signature(path, 'GET'))

        # timelog('%s > %s'%(path, params))
        url = 'https://api.naver.com%s'%(path)
        if params is not None and 0<len(params) :
            url += '?%s'%('&'.join(['%s=%s'%(k,str(v) if v is not None else '') for k,v in params.items()]))
        resp = self.session.get(url, timeout=30)

        return resp.json()

    def call_adkeyword(self, group_id) :
        self.session.headers.update(**self._signature('/ncc/keywords', 'GET'))
        resp = self.session.get('https://api.naver.com/ncc/keywords?nccAdgroupId=%s&recordSize=1000'%(group_id))
        return resp.json()

    @staticmethod
    def _parse_campaign_data(cdata) :
        has_period = cdata['usePeriod'] if 'usePeriod' in cdata else False
        _from = cdata['periodStartDt'].split('T')[0] if has_period and 'periodStartDt' in cdata else None
        _till = cdata['periodStartDt'].split('T')[0] if has_period and 'periodStartDt' in cdata else None
        _status = 0
        if cdata['status'] == 'ELIGIBLE' :
            today = datetime.today()
            if not(has_period and \
                (today < datetime.strptime(_from, '%Y-%m-%d') or datetime.strptime(_till, '%Y-%m-%d') < today)) :
                _status = 1
        elif cdata['status'] == 'DELETED' :
            _status = -1

        has_dailycap = cdata['useDailyBudget'] if 'useDailyBudget' in cdata else False
        _dailycap = cdata['dailyBudget'] if has_dailycap else None

        return {
            'cid': cdata['nccCampaignId'],
            'title': cdata['name'],
            'period_from': _from,
            'period_till': _till,
            'spending': cdata['totalChargeCost'],
            'status': _status,
            'account': cdata['customerId'],
            'user_lock': cdata['userLock'],
            'campaign_type': cdata['campaignTp'],
            'delivery': cdata['deliveryMethod'],
            'tracking': cdata['trackingMode'],
            'dailycap': _dailycap,
        }

    @staticmethod
    def _parse_adgroup_data(grp) :
        try :
            return {
                'gid': grp['nccAdgroupId'],
                'name': grp['name'],
                'gtype': grp['adgroupType'],
                'status': grp['status'],
                'bid_cap': grp['bidAmt'],
                'daily_cap': grp['dailyBudget'],
                'rolling': grp['adRollingType'],
                'target': grp['targets'] if 'targets' in grp else None,
            }
        except Exception as ex:
            timelog(ex)

    @staticmethod
    def _parse_adproduct_data(ad) :
        try :
            return {
                'id': ad['nccKeywordId'],
                'ad_keyword': ad['keyword'],
                'ad_creative': ad['nccKeywordId'],
                'links': ad['links'],
                'bid_cap': ad['bidAmt'],
                'client': ad['customerId'],
                'ratings': ad['nccQi']['qiGrade'],
                'status': ad['status'],
                'created_at': ad['regTm'],
                'updated_at': ad['editTm'],
            }
        except Exception as ex:
            print(ad)
            timelog(ex)

    @staticmethod
    def _parse_adstat_data(stat, ad) :
        try :
            rs = {
                'impressions': stat['impCnt'],
                'clicks': stat['clkCnt'],
                'conversions': stat['ccnt'],
                'cost': stat['salesAmt'],
                'avg_rank': stat['avgRnk'],
                'day_id': stat['dateStart'],
                'views': stat['viewCnt'],
            }
            rs.update(stats=json.dumps(rs))
            rs.update(**ad)
            return rs
        except :
            traceback.print_exc()
            print(stat)

    def retrieve_campaigns(self) :
        campaigns = []
        channels = {}
        for cdata in self.call('/ncc/campaigns') :
            campaigns.append(self._parse_campaign_data(cdata))

        # load adgroups
        for c in campaigns :
            cid = c['cid']
            groups = []
            for grp in self.call('/ncc/adgroups', nccCampaignId=cid) :
                groups.append(self._parse_adgroup_data(grp))
            time.sleep(0.25)
            c.update(groups=groups)
        campaign.saves(campaigns, **self.__common_args__)

    

    def _retrieve_record_stats(self, ads, sp) :
        for ad_id, ad in ads.items() :
            p = sp.copy()
            p.update(id=ad_id)

            stat_call = self.call('/stats', **p)
            puts = [self._parse_adstat_data(d, ad) for d in stat_call['data']]
            record.saves(puts)

        

    def retrieve_records(self, _from=None, _till=None) :
        campaigns = campaign.list_for_records(self.account_id, 'naver', 'search', _from, _till)

        stat_params = {
            'fields': json.dumps(['impCnt','clkCnt','salesAmt','avgRnk','ccnt','viewCnt']),
            'timeIncrement': 1,
            'timeRange': json.dumps({
                'since': _from if _from is not None else (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'until': _till if _till is not None else datetime.today().strftime('%Y-%m-%d'),
            })
        }       
        for cd in campaigns :
            timelog('campaign %d:%s open'%(cd['id'], cd['cid']))
            for g in self.call('/ncc/adgroups', nccCampaignId=cd['cid']) :
                try :
                    grp = self._parse_adgroup_data(g)
                    _ads = self.call_adkeyword(grp['gid'])
                    ads = {a['id']: a for a in map(self._parse_adproduct_data, _ads)}
                    for aid in ads.keys() :
                        ads[aid].update(
                            campaign_id=cd['id'],
                            group_id=grp['gid'],
                            title=grp['name'],
                            ad_group=grp['name'],
                            ad_product=grp['gtype'],
                            bid_cap=grp['bid_cap'],
                            daily_cap=grp['daily_cap'],
                            rolling=grp['rolling'],
                            target=grp['target'],
                        )
                    self._retrieve_record_stats(ads, stat_params)
                    
                    timelog('adgroup %s with %d ads'%(grp['gid'], len(ads)))
                except :
                    traceback.print_exc()
                time.sleep(0.5)
    
    def process(self) :
        # list campaigns
        self.retrieve_campaigns()

        # load values
        self.retrieve_records()


# test
if __name__ == '__main__' : 
    browser.console()
    exit(1)

