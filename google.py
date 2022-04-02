#! -*- coding: utf8 -*-

import re
import os
import time
import json
from datetime import datetime, timedelta

from dbproj.collector import timelog, worker, chrome_worker
from dbproj.models import campaign, record



class browser(chrome_worker) :
    def __init__(self, mode_debug=False) :
        super().__init__('google', mode_debug)

    __tasks__ = {
        'login': {
            'location': 'https://accounts.google.com/signin/v2/identifier?service=adwords',
            'script': '''(function() { })''',
            'post_condition': '''return (function() {
                return /accounts\.google/i.test(location.hostname);
            })();''',
        },
        'login_user': {
            'pre_condition': '''return (function() {
                let email_form = document.querySelector('input[type="email"]');
                let next_btn = document.querySelector('input[type="submit"]') || document.querySelector('[id*="next"]') || document.querySelector('[id*="Next"]');
                let username = `%s`;
                if(email_form && !email_form.getAttribute('aria-hidden')) {
                    email_form.value = username;
                }
                return email_form && !!email_form.value && !!next_btn;
            })()''',
            'script': '''(function() {
                let next_btn = document.querySelector('input[type="submit"]') || document.querySelector('[id*="next"]') || document.querySelector('[id*="Next"]');
                next_btn.click();
            })();'''
        },
        'login_pass': {
            'pre_condition': '''return (function() {
                let pass_form = document.querySelector('input[type="password"]');
                let password = `%s`;
                if(pass_form && !pass_form.getAttribute('aria-hidden')) {
                    pass_form.value = password;
                }

                let next_btn = document.querySelector('input[type="submit"]') || document.querySelector('[id*="next"]') || document.querySelector('[id*="Next"]');
                return pass_form && !!pass_form.value && !!next_btn
            })();''',
            'script': '''(function() {
                let next_btn = document.querySelector('input[type="submit"]') || document.querySelector('[id*="next"]') || document.querySelector('[id*="Next"]');
                next_btn.click();
            })();''',
        },
        'verify': {
            'script': '''return (function() {
                return /accounts\./.test(location.hostname) 
                    && /challenge/.test(location.pathname);
            })()''',
        },
        'verify_phone': {
            'pre_condition': '''return (function() {
                return !!document.querySelector('input[type="tel"]');
            })();''',
            'script': '''(function() {
                let country = document.querySelector('select[name*="country"]').value = `%s`;
                let put = document.querySelector('input[type="tel"]');
                put.value = `%s`;
                let next_btn = document.querySelector('input[type="submit"]') || document.querySelector('[id*="next"]') || document.querySelector('[id*="Next"]');
                next_btn.click();
            })()''',
        },
        'verify_pin': {
            'pre_condition': '''return (function() {
                return !!document.querySelector('#pin');
            })();''',
            'script': '''(function() {
                document.querySelector('#pin').value = `%s`;
                document.querySelector('#submit').click();
            })();''',
        },

        'reports': {
            'location': 'https://ads.google.com/aw/reporting/reporteditor/view?ocid=%s&reportId=%s',
            'script': '''(function() {
                let option_click = (function(label_pattern, option_selector) {
                    let checked = false;
                    let options = document.querySelectorAll(option_selector);
                    options.forEach((opt) => {
                        if(!checked) {
                            let label = opt.textContent.trim();
                            if(label_pattern.test(label)) {
                                opt.click();
                                checked = true;
                            }
                        }
                    });
                });
                let popup_option = (function(label_pattern, option_selector, popup_selector, btn_selector) {
                    return new Promise((rs) => {
                        let __interval = setInterval(()=>{
                            if(document.querySelector(popup_selector)) {
                                option_click(label_pattern, `${popup_selector} ${option_selector}`);
                                clearInterval(__interval);
                                rs();
                            } else {
                                document.querySelector(btn_selector).click();
                            }
                        }, 500);
                    });
                });

                // date-range last 7 days
                option_click(/7/, 'date-range-editor .item');
                // item count range 500
                popup_option(/500/, '.item', 'material-list[role="listbox"]', 'report-pagination-bar material-dropdown-select dropdown-button div');
            })();'''
        },
        'report_data': {
            'pre_condition': '''return (function() {
                let table = document.querySelector('ess-table .ess-table-canvas');

                return table && !table.getAttribute('aria-busy');
            })();''',
            'script': '''return (function() {
                const adtype_map = {
                    '검색': 'search',
                    '디스플레이': 'display',
                    '쇼핑': 'shopping',
                    '네트워크': 'network',
                    '동영상': 'video',
                    '유니버설 앱': 'universal app',
                    '호텔': 'hotel'
                };
                let _adtype = ((text) => {
                    if(!text) return 'search';

                    return Object.keys(adtype_map)
                        .filter((token) => 0<=text.indexOf(token))
                        .map((key) => adtype_map[key])
                        .join(' ');
                });
                let _status = ((text) => {
                    switch(text) {
                        case '운영중': return 1;
                        case '삭제됨': return -1;
                        default: return 0;
                    }
                });
                let _int = ((vs) => {
                    if(!vs) return 0;
                    let v = parseInt(vs.replace(/[^\d]+/g, ''));
                    if(isNaN(v)) return 0;
                    return v;
                });
                let _real = ((vs) => {
                    if(!vs) return 0;
                    let v = parseFloat(vs.replace(/[^\d\.]+/g, ''));
                    if(isNaN(v)) return 0;
                    return v;
                });
                let _date = ((vs) => {
                    let d = new Date(vs);
                    if(isNaN(d)) return null;
                    let mt = /\d+-\d+-\d+/.exec(d.toISOString())
                    return mt ? mt[0] : null;
                });

                let interval_out = 2000;
                let __interval = setInterval(() => {
                    interval_out -= 1;
                    let scrollpane = document.querySelector('.base-root');
                    let scrollHeight = scrollpane.scrollHeight;
                    let bodyHeight = document.body.clientHeight;
                    // scrolldown
                    scrollpane.scrollTop += 0.75*bodyHeight;

                    if(scrollHeight - bodyHeight <= scrollpane.scrollTop || interval_out<0) {
                        clearInterval(__interval);

                        let the_table = document.querySelector('ess-table .ess-table-canvas');
                        let values = [];
                        the_table.querySelectorAll('.particle-table-row[role="row"]')
                        .forEach((row) => {
                            try {
                                let r = {};
                                row.querySelectorAll('ess-cell').forEach((cell) => {
                                    let ky = cell.getAttribute('essfield').trim();
                                    let v = cell.textContent.trim();
                                    if(ky=='Ad') {
                                        if(cell.querySelector('.headline'))
                                            r.Headline = cell.querySelector('.headline').textContent.trim();
                                        if(cell.querySelector('.headline .link[href]'))
                                            r.AdLink = cell.querySelector('.headline .link').href;
                                        if(cell.querySelector('.visurl'))
                                            r.DisplayUrl = cell.querySelector('.visurl').textContent.trim();
                                        if(cell.querySelector('.description'))
                                            r.Description = cell.querySelector('.description').textContent.trim();

                                    } else {
                                        r[ky] = v;
                                    }
                                });
                                let ret = {
                                    day_id: _date(r.Day),
                                    account: r.Account,
                                    cid: r.ExternalCampaignId,
                                    campaign: r.Campaign,
                                    budget: _int(r.Budget),
                                    campaign_type: _adtype(r.CampaignType),
                                    period_from: _date(r.CampaignStartDate),
                                    period_till: _date(r.CampaignEndDate),
                                    adgroup_id: r.ExternalAdGroupId,
                                    adgroup: r.AdGroup,
                                    ad_id: r.ExternalAdId,
                                    content: r.Ad,
                                    agency: r.PrimaryCompanyName,
                                    adtype: r.AdType,
                                    ratings: _int(r.QualityScore),
                                    network: r.Network,
                                    ad_creative: r.Headline,
                                    ad_keyword: r.Keyword,
                                    bid_strategy: r.CampaignBidStrategyType,
                                    campaign_status: _status(r.CampaignStatus),
                                    group_status: _status(r.AdGroupStatus),
                                    display_status: r.CampaignPrimaryDisplayStatus,
                                    ad_status: r.AdPrimaryDisplayStatus,
                                    landing_url: r.AdLink,
                                    display_url: r.DisplayUrl, 
                                    description: r.Description,
                                    group_display: r.AdGroupPrimaryDisplayStatus,
                                    conversions: _real(r.ConversionsManyPerClick),
                                    impressions: _int(r.Impressions),
                                    clicks: _int(r.Clicks),
                                    cost: _int(r.Cost),
                                    views: _int(r.Views),
                                    interactions: _int(r.Interactions),
                                    engagement: _int(r.Engagements),
                                    bounce_rate: _real(r.BounceRate)/100,
                                    duration_seconds: _int(r.AverageVisitDuration),
                                };
                                values.push(ret);
                            } catch (ex) {
                                console.error(ex);
                            }
                        });

                        window.__report_data = values;
                    }
                }, 5);
            })();''',
        },


    }

    def intro(self) :
        # setup and login
        login_task = self.__tasks__['login'].copy()
        uname_task = self.__tasks__['login_user'].copy()
        upass_task = self.__tasks__['login_pass'].copy()

        self.proceed_task(**login_task, log='login')
        uname_task.update(pre_condition=uname_task['pre_condition']%(self.login))
        upass_task.update(pre_condition=upass_task['pre_condition']%(self.password))
        self.proceed_task(**uname_task, log='login.user')
        self.proceed_task(**upass_task, log='login.pass')

        verify_task = self.__tasks__['verify'].copy()
        verify_phone = self.__tasks__['verify_phone'].copy()
        verify_pin = self.__tasks__['verify_pin'].copy()
        while self.proceed_task(**verify_task, log='login.verify') :
            phone = input('phone> ').strip()
            self.proceed_task(**verify_phone, params=('KR', phone,), log='login.verify.phone')
            pins = input('pins> ').strip()
            self.proceed_task(**verify_pin, params=(pins,), log='login.verify.pin')

        # complete
    
    def authorization(self) :
        self.intro()


    @classmethod
    def extract_values(cls, d:dict, keys, **parsers) :
        v = {k:d[k] if k in d else None for k in keys}
        for k,fn in parsers.items() :
            v[k] = fn(d)
        return v

    __campaign_keys = (
        'cid',
        'agency',
        'account',
        'period_from',
        'period_till',
        'campaign_status',
        'budget',
    )

    @classmethod
    def extract_campaigns(cls, records) :
        campaigns = {}
        for rec in records :
            cid = rec['cid'] if 'cid' in rec else None
            if cid in campaigns : continue
            campaigns[cid] = cls.extract_values(rec, 
                keys=cls.__campaign_keys,
                ad_type=lambda v: v['campaign_type'] if 'campaign_type' in v else None,
                title=lambda v: v['campaign'] if 'campaign' in v else None, 
                status=lambda v: v['campaign_status'] if 'campaign_status' in v else None,
                spending=lambda v: v['budget'] if 'budget' in v else None)
        return campaigns

    __record_keys = (
        'day_id',
        'ad_creative',
        'ad_keyword',
        'impressions',
        'clicks',
        'cost',
    )
    __record_stat_keys = (
        'adgroup_id',
        'adgroup',
        'ad_id',
        'content',
        'adtype',
        'ratings',
        'network',
        'bid_strategy',
        'campaign_status',
        'group_status',
        'display_status',
        'ad_status',
        'landing_url',
        'display_url',
        'description',
        'group_display',
        'conversions',
        'impressions',
        'clicks',
        'cost',
        'views',
        'interactions',
        'engagement',
        'bounce_rate',
        'duration_seconds',
    )

    @classmethod
    def extract_record(cls, record) :
        return cls.extract_values(record, 
            keys=cls.__record_keys,
            title=lambda r: r['adgroup'] if 'adgroup' in r else None,
            ad_type=lambda r: r['campaign_type'] if 'campaign_type' in r else None,
            ad_product=lambda r: r['adtype'] if 'adtype' in r else None,
            ad_group=lambda r: r['adgroup'] if 'adgroup' in r else None,
            stats=lambda r: json.dumps(cls.extract_values(r, keys=cls.__record_stat_keys)))

    def data_transaction(self, records) :
        campaigns = self.extract_campaigns(records)
        put_campaigns = [c for c in campaigns.values()]
        campaign.saves(put_campaigns, 
            account_id=self.account_id, 
            ad_channel='google'
        )

        cid_map = campaign.cid_map(self.account_id, *campaigns.keys())
        puts = []
        for rec in records :
            cid = rec['cid']
            if cid not in cid_map : continue
            if rec['day_id'] is None : continue
            r = self.extract_record(rec)
            r.update(campaign_id=cid_map[cid])
            puts.append(r)
        record.saves(puts)


    @property
    def report_location(self) :
        return 'https://ads.google.com/aw/reporting/reporteditor/view?ocid=%s&reportId=%s'%(
            self.api_info['ocid'],
            self.api_info['report_id'])


    def process(self) :
        self.intro()

        time.sleep(0)

        task = self.__tasks__['reports'].copy()
        task.update(location=self.report_location, log='reports')
        # move to report page then wait
        report_title = self.proceed_task(**task)
        time.sleep(1)

        data_task = self.__tasks__['report_data'].copy()
        pagenum = 0
        while True :
            pagenum += 1
            recs = self.retrieve_values('report_data', log='page %s'%(pagenum))
            self.data_transaction(recs)
            
            # move next page
            next_btn = self.proceed_task(script='''
                // clear front data
                window.__report_data = null;
                let next_btn = document.querySelector('material-button.next');
                if(next_btn && !next_btn.classList.contains('is-disabled')) {
                    next_btn.click();
                    return true;
                } else {
                    return false;
                }''')
            
            if not next_btn : break
            
        self.driver.close()


if __name__ == '__main__' : 
    browser.console()
    exit(1)
