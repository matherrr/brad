#! -*- coding: utf8 -*-

import sys
import json
import traceback
import time

from datetime import datetime, timedelta

from dbproj.collector import timelog, worker, chrome_worker, requests_worker
from dbproj.models import account, campaign, record

class browser(chrome_worker) :
    __tasks__ = {
        'login': {
            'location': 'https://nosp.da.naver.com/center/login/form',
            'pre_condition': '''return !!document.querySelector('iframe[src*="/login"]');''',
            'script': '''
                let frm = document.querySelector('iframe[src*="/login"]');
                let fdoc = frm.contentDocument;
                fdoc.forms.frm.userId.value = `%s`;
                fdoc.forms.frm.userPw.value = `%s`;
                fdoc.forms.frm.submit();
            ''',
            'post_condition': '''return /\/home\//.test(location.pathname)''',
        },
        'intro': {
            'pre_condition': '''return !!document.querySelector('a[href*="/center/report/campaign"]')''',
            'script': '''document.querySelector('a[href*="/center/report/campaign"]').click();''', 
            'post_condition': '''return /\/report\/campaign\//.test(location.pathname)''',
        },
        'campaigns_prepare': {
            'location': 'https://report.da.naver.com/campaign/list',
            'pre_condition': '''
                return !!window.$;
            ''',
            'script': ''' (function() {
                // ready for campaigns
                window.__campaigns = [];
                let page = 0;
                let loadingLock = false;
                let max_retries = 10;
                let closing = function() {
                    clearInterval(window.__campaigns_interval);
                    window.__campaigns_interval = null;
                }
                
                window.__campaigns_interval = setInterval(() => {
                    if(loadingLock) return;

                    loadingLock = true;
                    let params = {
                        searchCampNm: null,
                        searchCampId: null,
                        reguserNm: null,
                        campstartYmdt: moment(`%s`).format('YYYY.MM.DD'),
                        campendYmdt: moment(`%s`).format('YYYY.MM.DD'),
                        sponsorNm: null,
                        brandNm: null,
                        bizcatNm: null,
                        _search: false,
                        nd: Date.now(),
                        rows: 40,
                        page: ++page,
                        sidx: null,
                        sord: null,
                    };
                    $.ajax({
                        url: '/campaign/list/data.json?_JSON-TYPE_-REQ_=Y&_JSON-TYPE_-REQ_=Y',
                        method: 'POST',
                        data: params,
                        dataType: 'json',
                        success: function(resp) {
                            if(resp.data && resp.data.list)
                                window.__campaigns = window.__campaigns.concat(resp.data.list);
                            if(!resp || !resp.data || !resp.data.totalPage || resp.data.totalPage < page)
                                closing();
                        }, 
                        error: function(err) {
                            console.error(err, max_retries);
                            max_retries -= 1;
                            if(max_retries < 0) 
                                closing();
                            else
                                page -= 1;
                        },
                        complete: function() { loadingLock = false; }
                    });
                }, 500);
            })();''',
            'post_condition': '''return !window.__campaigns_interval''',       
        },
        'campaigns': {
            'script': '''let now = moment();
            return JSON.stringify(
                window.__campaigns.map((cmp) => {
                    let _from = moment(cmp.lcampstartYmdt);
                    let _till = moment(cmp.lcampendYmdt);                    
                    return {
                        cid: cmp.campId,
                        spending: cmp.campMny,
                        title: cmp.campNm,
                        agency: cmp.repNm || cmp.agentNm,
                        brand: cmp.brandNm,
                        account: cmp.sponsorNm,
                        category: cmp.bizcatNm,
                        period_from: _from.format('YYYY-MM-DD hh:mm:ss'),
                        period_till: _till.format('YYYY-MM-DD hh:mm:ss'),
                        is_new: cmp.newUnitYn == 'Y',
                        user_name: cmp.reguserNm,
                        _version: cmp.repoVer,
                        _statcd: cmp.statCd,
                        status: _from.isBefore(now) && _till.isAfter(now) ? 1 : 0,
                        info: JSON.stringify(cmp),
                    }
                })
            );'''
        },
        'reports': {
            'pre_condition': '''
                if(document.querySelector('#reportPage a.more_next'))
                    document.querySelector('#reportPage a.more_next').click();
                return !!(document.querySelector('#indicatorBody') && document.querySelector('#indicatorBody').innerHTML.length);
            ''',
            'script': '''(async function() {
                const dim_select = ['광고상품', '상품유형', '광고소재요소', '키워드', '일자', '광고소재'];
                const met_select = ['집행금액', '광고비', '노출수', '클릭수', '도달수', '랜딩 클릭수', '3초 재생수', '10초 재생수'];
                const day_select = '지난7일';

                let _progress = (function() {
                    return new Promise((rs) => {
                        let __p_interval = setInterval(() => {
                            if(document.querySelector('#progressBarPop').style.display != 'none') return;
                            clearInterval(__p_interval);
                            rs();
                        }, 50);
                    })
                });

                let next_page = (function() {
                    let nxt = document.querySelector('#reportPage .on');
                    if(nxt) nxt = nxt.nextElementSibling;
                    if(nxt) nxt.click();
                    return !!nxt;
                });

                let update_options = (function(sels) {
                    let dselects = document.querySelector('#selectorDialog');
                    return new Promise((rs) => {
                        let __u_interval = setInterval(() => {
                            if(dselects.style.display!='none') {
                                clearInterval(__u_interval);
                                dselects.querySelectorAll('#selectorBox ul li a._item').forEach((item) => {
                                    let label = item.textContent.trim();
                                    let to_set = 0<=sels.indexOf(label);
                                    let has_set = item.classList.contains('checked');
                                    if(to_set != has_set)
                                        item.click();
                                });
                                dselects.querySelector('.btnBox .btnSelectorComplete').click();
                                rs();
                            }
                        });
                    });
                });

                // update dimensions
                document.querySelector('a.itemOpen[item-type="dimension"]').click();
                await update_options(dim_select);

                // update metrics
                document.querySelector('a.itemOpen[item-type="indicator"]').click();
                await update_options(met_select);

                await _progress();

                // update calendar date
                (function() {
                    document.querySelector('#ui-datepicker-div').click();
                    let calendar = document.querySelector('.report-daterangepicker');
                    calendar.querySelectorAll('.report-daterangepicker-presetsmenu li.ui-menu-item').forEach((item) => {
                        let label = item.textContent.trim();
                        if(day_select == label && !item.classList.contains('ui-state-highlight'))
                            item.click();
                    });
                    calendar.querySelector('button.report-daterangepicker-applybutton').click();
                })();

                await _progress();

                // retrieve values
                (function() {
                    let dimensions = [];
                    document.querySelectorAll('#dimensionHeader table th').forEach((th, di) => {
                        dimensions[di] = th.textContent.replace(/\s/g,'');
                    });

                    let metrics = [];
                    document.querySelectorAll('#indicatorHeader table th').forEach((th, di) => {
                        metrics[di] = th.textContent.replace(/\s/g, '');
                    });

                    let report_data = [];

                    new Promise(async function(resolve) {
                        do {
                            await _progress();

                            let entries = [];
                            document.querySelectorAll('#dimensionBody table tbody tr').forEach((tr, ri) => {
                                let e = entries[ri] || {};
                                tr.querySelectorAll('td').forEach((td,di) => {
                                    if(dimensions[di] && td.textContent)
                                        e[dimensions[di]] = td.textContent.trim();
                                });
                                entries[ri] = e;
                            });
                            document.querySelectorAll('#indicatorBody table tbody tr').forEach((tr, ri) => {
                                let e = entries[ri] || {};
                                tr.querySelectorAll('td').forEach((td,di) => {
                                    if(metrics[di] && td.textContent) {
                                        let tv = td.textContent.trim();
                                        if(/\d*\.\d*/.test(tv))
                                            e[metrics[di]] = parseFloat(tv);
                                        else if(/(\d{1,3},?)+/.test(tv))
                                            e[metrics[di]] = parseInt(tv.replace(/[^\d]/g, ''));
                                        else
                                            e[metrics[di]] = tv;
                                    }
                                });
                                entries[ri] = e;
                            });

                            report_data = report_data.concat(entries.map((e) => {
                                rs = {
                                    day_id: e.일자,
                                    ad_product: e.광고상품,
                                    ad_group: e.광고소재요소,
                                    ad_creative: e.광고소재,
                                    ad_keyword: e.키워드,
                                    impressions: e.노출수,
                                    clicks: e.클릭수,
                                    cost: e.광고비,
                                    stats: JSON.stringify(e),
                                }
                                return rs;
                            }));
                        } while(next_page());
                        window.__reports = report_data;
                        resolve(report_data);
                    });
                })();
            })();''',
        }
    }

    def __init__(self, mode_debug=False) :
        super().__init__('nosp', mode_debug)

    def intro(self) :
        # login
        task_login = self.__tasks__['login'].copy()
        task_login.update(params=(self.login, self.password))
        self.proceed_task(**task_login)

    def retrieve_campaigns(self, period_from=None, period_till=None) :
        # setting up period
        _from = period_from if period_from is not None else datetime.today() - timedelta(days=7)
        _till = period_till if period_till is not None else datetime.today() + timedelta(days=7)
        def __list_campaigns_prepare_params(args) :
            args.update(params=(_from, _till))
            return args

        # loading accounts
        (task_prepare, task_retrieve) = worker.list_tasks(self.__tasks__, 
            ('campaigns_prepare', 'campaigns'),
            campaigns_prepare=__list_campaigns_prepare_params)
        self.proceed_task(**task_prepare)

        campaigns = self.proceed_task(**task_retrieve)
        # parse json
        campaigns = json.loads(campaigns)
        campaign.saves(campaigns, account_id=self.account_id, ad_channel='naver', ad_type='display')

        timelog('Campaigns updated %s'%(str(tuple([c['cid'] for c in campaigns]))))

    def retrieve_records(self) :
        for cmp in campaign.by_account(self.account_id) :
            if 0<cmp['status'] :
                try :
                    _recs = self.retrieve_values('reports', location='https://report.da.naver.com/report/main/?campId=%s&rptNo=1000001'%(cmp['cid']))
                    record.saves(_recs, campaign_id=cmp['id'], title=cmp['title'])
                except :
                    traceback.print_exc()
                    continue

    def process(self) :
        self.intro()

        self.retrieve_campaigns()

        self.retrieve_records()

if __name__ == '__main__' : 
    browser.console()
    exit(1)