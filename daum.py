#! -*- coding: utf8 -*-

import json
from dbproj.collector import worker, chrome_worker, timelog
from dbproj.models import campaign, record

"""
/modifyuser/changepwguideview.daum?

document.querySelector('input#sevendays').checked = true;
"""

class browser(chrome_worker) :
    def __init__(self, mode_debug=False) :
        super().__init__('daum', mode_debug)

    __tasks__ = {
        'login': {
            'location': 'https://clixagency.biz.daum.net/login',
            'pre_condition': '''return !!document.forms.loginForm''',
            'script': '''(function() {
                document.forms.loginForm.querySelector('input#userId').value = `%s`;
                document.forms.loginForm.querySelector('input#userPw').value = `%s`;
                document.forms.loginForm.submit();
            })();''',
            'post_condition': '''return !/\/login/.test(location.pathname)''',
        },
        'accounts': {
            'location': 'https://clixagency.biz.daum.net/manage/search',
            'pre_condition': '''return !!document.querySelector('table.tbl_comm');''',
            'script': '''(async function() {
                window.__accounts = null;

                let _progress = (function() {
                    let _interval = 100;
                    return new Promise((rs) => {
                        let __progress_interval = setInterval(()=>{
                            let progress = document.querySelector('.spinner_wrap');
                            if(!progress) {
                                clearInterval(__progress_interval);
                                rs(true);
                            }
                        });
                    });
                });

                accounts = {};

                await _progress();

                document.querySelectorAll('table.tbl_comm tbody tr:not(.over)').forEach((row) => {
                    let ln = row.querySelector('a[href*="mbrseq"]');
                    let txt = ln.textContent.trim();
                    let grp = /^(?<a>.+)\s*\((?<c>[^\(\)]+)\)$/.exec(txt)
                    let ret = {
                        mid: row.querySelector('input[value]').value,
                        id: /mbrseq=(?<v>[\d]+)/.exec(ln.search).groups.v,
                        name: grp ? grp.groups.a.trim() : txt,
                        code: grp ? grp.groups.c : null,
                        href: ln.href
                    };

                    accounts[parseInt(ret.id)] = ret;
                });

                window.__accounts = accounts;
            })();''',
        },
        'campaigns': {
            'pre_condition': '''return !!document.querySelector('table.tbl_comm');''',
            'script': '''(async function() {
                window.__campaigns = null;

                let _progress = (function() {
                    let _interval = 100;
                    return new Promise((rs) => {
                        let __progress_interval = setInterval(()=>{
                            let progress = document.querySelector('.spinner_wrap');
                            if(!progress) {
                                clearInterval(__progress_interval);
                                rs(true);
                            } 
                        });
                    });
                });

                let maximize_counts = (function() {
                    return new Promise((rs) => {
                        let option_clicked = false;
                        let __tb_opt_interval = setInterval(() => {
                            let tab_panel = document.querySelector('#adManagementTabPage');
                            let table_options =  tab_panel.querySelectorAll('.wrap_tableoption .box_opt');
                            let last_opt = table_options[table_options.length-1];
                            let opt_list = last_opt.querySelector('ul.list_optlayer');
                            let opt_base = last_opt.querySelector('.opt_base');

                            if(opt_list) {
                                clearInterval(__tb_opt_interval);

                                let to_set = opt_list.querySelector('li:last-child a');
                                if(opt_base.textContent.indexOf(to_set.textContent.trim()) <0) {
                                    to_set.click();
                                    rs(to_set);
                                } else {
                                    opt_base.click();
                                    rs(false);
                                }
                            } 
                            else if(!option_clicked) {
                                last_opt.querySelector('.opt_base').click();
                                option_clicked = !option_clicked;
                            }
                        }, 100);
                    });
                });

                let move_next_page = (function() {
                    if(!document.querySelector('.paging em.btn_page')) return null;
                    let next = document.querySelector('.paging em.btn_page').nextElementSibling;
                    if(next)
                        next.click();
                    return !!next;
                });

                let set_campaigns_tab = (function() {
                    document.querySelector('#adManagementTabHeader .tab_comm[href$="/ad/campaigns"]').click();
                });

                let set_adgroups_tab = (function() {
                    document.querySelector('#adManagementTabHeader .tab_comm[href$="/ad/ad-groups"]').click();
                });

                let cell_int = (function(cell) { return parseInt(cell.textContent.replace(/[^\d]+/g,'')); });

                let __retrieve_table_values = (function(retrieve_fn) {
                    let table = document.querySelector('table.tbl_comm');
                    let rows = table.querySelectorAll('tbody tr');
                    let rets = [];
                    rows.forEach((r) => {
                        rets.push(Object.assign(retrieve_fn(r), {
                            id: r.querySelector('input.inp_check').value,
                            name: r.querySelector('td.fst .txt').textContent.trim(),
                            status: /ON/i.test(r.querySelector('td:nth-child(2)').textContent),
                        }));
                    });
                    return rets;
                });

                let retrieve_campaign_values = (function() {
                    return __retrieve_table_values((r) => {
                        let cells = r.querySelectorAll('td');
                        let cname = r.querySelector('a.campaign_name').textContent;
                        let cid = r.querySelector('input[name="campaignSeq"]').value;
                        return {
                            cid: parseInt(cid),
                            name: cname.trim(),
                            day_spending: cell_int(cells[3]),
                            daily_cap: cell_int(cells[4]) || null,
                            impressions: cell_int(cells[5]) || null,
                            groups: {},
                        }
                    });
                });

                let retrieve_adgroup_values = (function() {
                    return __retrieve_table_values((r) => {
                        let cells = r.querySelectorAll('td');
                        let cpath = r.querySelector('.campaign a').pathname;
                        let gname = r.querySelector('a.adgroup_name').textContent;

                        return {
                            name: gname.trim(),
                            cid: /\/(?<v>[\d]+)/.exec(cpath).groups.v,
                            daily_cap: cell_int(cells[4]) || null,
                            day_spending: cell_int(cells[5]),
                            impressions: cell_int(cells[6]) || null,
                        }
                    });
                });

                /* __main__ */
                await _progress();

                let campaigns = {};

                set_campaigns_tab();
                await _progress();
                await maximize_counts();
                do {
                    await _progress();
                    retrieve_campaign_values().forEach((cmp) => {
                        campaigns[cmp.id] = cmp;
                    });
                } while(move_next_page());

                set_adgroups_tab();
                await _progress();
                await maximize_counts();
                do {
                    await _progress();
                    retrieve_adgroup_values().forEach((grp) => {
                        let cid = grp.cid.toString();
                        let gid = grp.id.toString();
                        campaigns[cid].groups[gid] = grp;
                    });
                } while(move_next_page());

                window.__campaigns = campaigns;
            })();''',
        },
        'marketers': {
            'location': 'https://clixagency.biz.daum.net/manage/report/manage/',
            'pre_condition': '''return !!document.querySelector('table.tbl_comm');''',
            'script': '''(async function() {
                window.__marketers = null;

                let _progress = (function() {
                    let _interval = 100;
                    return new Promise((rs) => {
                        let __progress_interval = setInterval(()=>{
                            let progress = document.querySelector('.spinner_wrap');
                            if(!progress) {
                                clearInterval(__progress_interval);
                                rs(true);
                            } 
                        });
                    });
                });

                let _group_option = (function(index) {
                    return new Promise((rs, rj) => {
                        let _grp_interval = setInterval(() => {
                            let boxsel = document.querySelector('#conditionReportTitle .box_select');
                            let box_base = boxsel.querySelector('.opt_base');
                            let box_list = boxsel.querySelector('.list_optlayer');

                            if(!box_list) {
                                box_base.click();
                            } else {
                                clearInterval(_grp_interval);
                                let options = box_list.querySelectorAll('li');
                                let to_select = options[index];
                                if(to_select)
                                    to_select.click();
                                rs(to_select);
                            }
                        }, 100);
                    });
                });

                let _option_values = (function() {


                });

                let move_next_page = (function() {
                    if(!document.querySelector('.paging em.btn_page')) return null;
                    let nxt = document.querySelector('.paging em.btn_page').nextElementSibling;
                    if(nxt)
                        nxt.click();
                    return !!nxt;
                });

                // hop in any marketer link
                await _progress();
                document.querySelector('table.tbl_comm tbody tr > td a.txt').click();
                await _progress();

                // load marketers
                let marketers = {}
                let index = 0;
                let pattern = /marketer\/(?<mid>[\d]+)\/member\/(?<aid>[\d]+)/;

                while(true) {
                    if(!await _group_option(index++)) 
                        break;
                    await _progress();

                    do {
                        let rows = document.querySelectorAll('#conditionReportBody tr');
                        rows.forEach((r) => {
                            let ln = r.querySelector('td a.txt[href]');
                            let mt = pattern.exec(ln);
                            if(mt) {
                                if(!marketers[mt.groups.mid]) {
                                    let txt = ln.textContent.trim();
                                    let grp = /^(?<a>.+)\s*\((?<c>[^\(\)]+)\)$/.exec(txt)
                                    marketers[mt.groups.mid] = {
                                        name: grp ? grp.groups.a : txt,
                                        code: grp ? grp.groups.c : null,
                                        accounts: []
                                    }
                                }
                                
                                marketers[mt.groups.mid].accounts.push(mt.groups.aid);
                            }
                        });
                    } while(move_next_page());
                }

                window.__marketers = marketers;
            })();''',
        },
        'records': {
            'pre_condition': '''return !!document.querySelector('table.tbl_comm');''',
            'script': '''(async function(dates) {
                window.__records = null;

                let dayset_up = (function(ds) {
                    return new Promise((rs) => {
                        let day_select = ds || '7일';
                        let opt_base = document.querySelector('#dateControl .opt_base');
                        
                        if(0<=opt_base.textContent.indexOf(day_select)) { rs(true); }
                        else {
                            let _day_interval = setInterval(() => {
                                let opt_list = document.querySelector('#dateControl .list_optlayer');
                                if(opt_list) {
                                    clearInterval(_day_interval);
                                    let found = false;
                                    opt_list.querySelectorAll('li[data-index]').forEach((op) => {
                                        if(!found && 0<=op.textContent.indexOf(day_select)) {
                                            found = true;
                                            op.click();
                                        }
                                    });
                                    rs(found);
                                } else {
                                    document.querySelector('#dateControl .opt_base').click();
                                }
                            }, 100);
                        }
                    });
                });

                let _progress = (function() {
                    let _interval = 100;
                    return new Promise((rs) => {
                        let __progress_interval = setInterval(()=>{
                            let progress = document.querySelector('.spinner_wrap');
                            if(!progress) {
                                clearInterval(__progress_interval);
                                rs(true);
                            } 
                        });
                    });
                });

                let _group_option = (function(index) {
                    return new Promise((rs) => {
                        let _grp_interval = setInterval(() => {
                            let boxsel = document.querySelector('#conditionReportTitle .box_select');
                            let box_base = boxsel.querySelector('.opt_base');
                            let box_list = boxsel.querySelector('.list_optlayer');

                            if(!box_list) {
                                box_base.click();
                            } else {
                                clearInterval(_grp_interval);
                                let options = box_list.querySelectorAll('li');
                                let to_select = options[index];
                                if(to_select)
                                    to_select.click();
                                rs(to_select);
                            }
                        }, 100);
                    });
                });

                let move_next_page = (function() {
                    if(!document.querySelector('.paging em.btn_page')) return null;
                    let nxt = document.querySelector('.paging em.btn_page').nextElementSibling;
                    if(nxt)
                        nxt.click();
                    return !!nxt;
                });

                // hop in any adgroup link
                await _progress();
                let hopin = document.querySelector('table.tbl_comm tbody tr > td a.txt');
                if(!hopin) {
                    window.__records = [];
                    return;
                }
                else {
                    hopin.click();
                    await _progress();
                }

                let record_values = (function() {
                    let vs = document.querySelectorAll('#trendReportTable tbody tr');
                    let rets = [];
                    vs.forEach((v) => {
                        rets.push({
                            day_id: v.querySelector('td:nth-child(1)').textContent.trim(),
                            impressions: cell_int(v.querySelector('td:nth-child(2)')) || 0,
                            clicks: cell_int(v.querySelector('td:nth-child(3)')) || 0,
                            cost: cell_int(v.querySelector('td:nth-child(6)')) || 0,
                            conversions: cell_int(v.querySelector('td:nth-child(7)')) || null,
                        });
                    });
                    return rets;
                })

                let cell_int = (function(cell) { return parseInt(cell.textContent.replace(/[^\d]+/g,'')); });

                let index = 0;
                let recs = [];

                dayset_up(dates);

                while(true) {
                    if(!await _group_option(index))
                        break;
                        
                    do {
                        await _progress();
                        rows = document.querySelectorAll('#conditionReportBody tr');
                        for(let i=0; i<rows.length; i++) {
                            let r = rows[i];
                            let on = /on/i.test(r.querySelector('td:nth-child(2)').textContent);
                            let imps = cell_int(r.querySelector('td:nth-child(3)'));
                            let ln = r.querySelector('td:first-child a[data-seq]');
                            if(imps) {
                                ln.click();
                                await _progress();
                
                                let rs = {
                                    id: ln.dataset.seq,
                                    keyword: ln.dataset.name,
                                    v: record_values(),
                                };
                                recs.push(rs);
                            }
                        }
                        // test break
                    } while(move_next_page());
                    index += 1;
                }
                window.__records = recs;
            })()''',
        },
    }

    def intro(self) : 
        if not self.has_account() :
            raise Exception('Account access required')
    
        login_task = self.__tasks__['login'].copy()
        login_task.update(params=(self.login, self.password))
        self.proceed_task(**login_task)


    def retrieve_accounts(self) :
        # load marketer info
        rss = self.retrieve_values('marketers')
        print(rss)

        # load account info
        accounts = self.retrieve_values('accounts')
        print(accounts)

        # mapping
        for mid, mdata in rss.items() :
            aids = mdata['accounts']
            mdata['accounts'] = list(
                map(lambda aid: accounts[aid],
                filter(lambda aid: aid in accounts, aids)))

        return rss

        
    def retrieve_campaigns(self, mid, aid, marketer, account) :
        # load campaigns
        campaigns = self.retrieve_values('campaigns', 
            location='https://clixagency.biz.daum.net/manage/member/ad/campaigns?mbrseq=%d'%(aid))
        puts = []
        cids = []
        for cid,cd in campaigns.items() :
            cid = int(cd['cid'])
            cids.append(str(cid))
            cd.update(marketer=marketer, account=account);
            puts.append({
                'cid': cid,
                'marketer': marketer,
                'client': account,
                'account': account['name'],
                'agency': marketer['code'],
                'brand': cd['name'],
                'title': cd['name'],
                'status': cd['status'],
            })
        campaign.saves(puts, 
            account_id=self.account_id, 
            ad_channel='daum', 
            ad_type='search')

    def retrieve_records(self, mid) :
        for c in campaign.with_daum(self.account_id, mid) :
            aid = c['info']['client']['id']
            cid = c['cid']
            records = self.retrieve_values('records',
                location='https://clixagency.biz.daum.net/manage/report/manage/marketer/%s/member/%s/campaign/%s'%(mid,aid,cid))
            for rdata in records :
                gid = int(rdata['id'])
                word = rdata['keyword']
                values = rdata['v']
                record.saves(values, campaign_id=c['id'], title=c['title'],
                    ad_product='search', ad_group=gid, ad_keyword=word)
            timelog('%s/%s/%s: %d'%(mid,c['account'],c['cid'], len(records)))

    def process(self) :
        self.intro()

        groups = self.retrieve_accounts()
        for mid, marketer in groups.items() :
            mid = int(mid)
            mdata = {
                'id': mid,
                'name': marketer['name'],
                'code': marketer['code']
            }
            # put campaign info
            for account in marketer['accounts'] :
                aid = int(account['id'])
                timelog('%d/%d: %s'%(mid, aid, str(account)))
                self.retrieve_campaigns(mid, aid, mdata, account)

            # run records            
            self.retrieve_records(mid)

    

if __name__ == '__main__' : 
    browser.console()
    exit(1)
    



    





        