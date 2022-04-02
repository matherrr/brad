#! -*- coding: utf8 -*-

import time
import json
import traceback

from dbproj.collector import timelog, worker, chrome_worker
from dbproj.models.segment import segment
from dbproj.models.performance import performance
from datetime import datetime, timedelta

class browser(chrome_worker) :
    __tasks__  = {
        #{'script', 'location', 'pre_condition', 'post_condition'}
        'login': {
            'location': r'https://adobeid-na1.services.adobe.com/renga-idprovider/pages/login?callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fadobeid%2FExperienceCloud_prod%2FAdobeID%2Fcode%3Fredirect_uri%3Dhttps%253A%252F%252Fexc-loginims.experiencecloud.adobe.com%252Fexc-session%252Flogin%253Fprovider%253DExperienceCloud_prod%2526prefixtenantid%253Dsamsungsec%2526redirectlocation%253D%2526resource%253D&client_id=ExperienceCloud_prod&scope=openid%2Cavatar%2Cread_organizations%2Cadditional_info.job_function%2Csession%2Cadditional_info.projectedProductContext%2Cadditional_info.account_type%2Cadditional_info.roles%2Cadditional_info.user_image_url%2Caudiencemanager_api%2CAdobeID&denied_callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fdenied%2FExperienceCloud_prod%3Fredirect_uri%3Dhttps%253A%252F%252Fexc-loginims.experiencecloud.adobe.com%252Fexc-session%252Flogin%253Fprovider%253DExperienceCloud_prod%2526prefixtenantid%253Dsamsungsec%2526redirectlocation%253D%2526resource%253D%26response_type%3Dcode&locale=en_US&flow_type=code&idp_flow_type=login',
            'pre_condition': '''
                return !!document.querySelector('#adobeid_signin');
            ''',
            'script': '''
                setTimeout(() => {
                    document.querySelector('#adobeid_signin input[name="username"]').value = `%s`;
                    document.querySelector('#adobeid_signin input[name="password"]').value = `%s`;
                    document.querySelector('#adobeid_signin button#sign_in').click();
                }, 500);
            ''',
        },
        'intro': {
            'pre_condition': ''' return !!/@.+\/home/i.test(location.hash); ''',
            'script': '''(async function() {
                let __interval = setInterval(function(){ 
                    let quicklink = document.querySelector('a.spectrum-Link[href*="analytics"]');
                    if(quicklink) {
                        quicklink.click();
                        clearInterval(__interval);
                        return;
                    } else {
                        let btn = document.querySelector('.spectrum-ShellContainer .solution-menu');
                        if(btn) btn.click();

                        let menu = document.querySelectorAll('ul.solutionSwitcher button.itemSwitcher.itemSwitcher--enabled');
                        menu.forEach(function(mitem) {
                            if(/analytics/i.test(mitem.textContent)) {
                                mitem.click();
                                clearInterval(__interval);
                            }
                        });
                        return;
                    }
                }, 500);
            })();'''
        },
        'analytics': {
            'pre_condition': ''' return /\.omniture/.test(location.hostname); ''',
            'script': '''setInterval(function() { location.hash = '#/components/segments'; }, 500)''',
        },
        'segments': {
            'pre_condition': '''
                let container = document.querySelector('.ComponentManager-tableContainer');
                let rtContainer = null;
                if(!container) return false;
                Object.keys(container).forEach((ck) => {
                    if(!rtContainer && ck.match(/__reactInternalInstance.+/)) {
                        rtContainer = container[ck];
                    }
                });
                return !!(rtContainer && rtContainer.child && rtContainer.child.pendingProps);''',
            'script': '''
                return JSON.stringify((function() {
                    let container = document.querySelector('.ComponentManager-tableContainer');
                    let rtContainer = null;
                    Object.keys(container).forEach((ck) => {
                        if(!rtContainer && ck.match(/__reactInternalInstance.+/)) {
                            rtContainer = container[ck];
                        }
                    });
                    let containerProps = rtContainer.child.pendingProps;
                    return containerProps.rowData
                        .map((seg) => seg._data)
                        .map((sd) => {
                            return {
                                id: sd.id,
                                approved: sd.approved,
                                favorite: sd.favorite,
                                deleted: sd.isDeleted,
                                modified: sd.modified.getTime(),
                                title: sd.name,
                                owner_id: sd.owner._data.id,
                                owner_login: sd.owner._data.login,
                                report_suite: sd.reportSuiteName,
                                rsid: sd.rsid,
                            }
                        });
                })());
            '''
        },
        'report': {
            'location': 'https://%s/%s',
            'script': '''
                let __dateInterval = setInterval(() => {
                    let calendarBtn = document.querySelector('#calendar-widget-content');
                    if(document.querySelector('.CalendarWidget')) {
                        let frm = document.querySelector('.CalendarWidget');
                        frm.querySelector('input[name="start"]').value = moment(`%s`).format('DD/MM/YYYY');
                        frm.querySelector('input[name="end"]').value = moment(`%s`).format('DD/MM/YYYY');
                        frm.querySelector('input.button[name="run"]').click();
                        clearInterval(__dateInterval);
                    } else if(calendarBtn) {
                        calendarBtn.click();
                    }
                }, 10);
            '''
        },
        'report_date': {
            'pre_condition': '''return !!document.querySelector('#calendar-widget-content')''',
            'script': '''
                let __dateInterval = setInterval(() => {
                    let calendarBtn = document.querySelector('#calendar-widget-content');
                    let _unix = moment(`%s 00:00:00+00:00Z`).unix()*1000;
                    let dday_selector = `td[abbr="${_unix}"]`;
                    if(!window.moment) {
                        return; 
                    }
                    else if(document.querySelector('.CalendarWidget')) {
                        let frm = document.querySelector('.CalendarWidget');
                        let dday = frm.querySelector(dday_selector);
                        let retries = 24;
                        let btn_cls = _unix < parseInt(frm.querySelector('td[abbr]').abbr) ? 'prev' : 'next';

                        while(!dday && 0<retries) {
                            frm.querySelector(`.monthSelector .${btn_cls}`).click();
                            dday = frm.querySelector(dday_selector);
                            retries -= 1;
                        }
                        if(dday) {
                            dday.click(); 
                            setTimeout(()=> { 
                                frm.querySelector('input.button[name="run"]').click();
                            }, 500);
                            clearInterval(__dateInterval);
                        } 
                    } else if(calendarBtn) {
                        calendarBtn.querySelector('[class*="Activator"]').click();
                    }
                }, 500);
            ''',
            'post_condition': '''return window.moment && 0<=location.search.indexOf(encodeURIComponent(moment(`%s`).format('MM/DD/YY')));'''
        },
        'report_data': {
            'pre_condition': '''
                if(document.body.dataset.angularLoaded)  {
                    return JSON.parse(document.body.dataset.angularLoaded);
                }
                else {
                    return false;
                }
            ''',
            'script': '''return (function() {
                    let tb = document.querySelector('#data_table > table');
                    if(!tb) return [];

                    let cmap = [];
                    // load column mapping
                    tb.querySelectorAll('tr.data_table_header > td').forEach((c) => {
                        let cname = c.textContent.trim();
                        if(!cname || cname.length<=0) cname = null;
                        let span = parseInt(c.getAttribute('colspan')) || 1;
                        cmap.push(cname);
                        for(let i=1; i<span; i++) { cmap.push(null); }
                    });

                    cmap = cmap.map((cname, ci) => {
                        if(!cname || cname.length<=0) return null;
                        switch(!!cname) {
                            case !!cname.match(/tracking code/i): 
                                return 'sid';
                            case !!cname.match(/page views/i):
                                return 'pageview';
                            case !!cname.match(/visits/i): 
                                return 'visits';
                            case !!cname.match(/cart add/i): 
                                return 'cart_add';
                            case !!cname.match(/order/i) && !!cname.match(/purchase event/i) :
                                return 'conversions';
                            case !!cname.match(/revenue/i) && !!cname.match(/purchase event/i) :
                                return 'value';
                            case !!cname.match(/bounces/i):
                                return 'bounces';
                            case !!cname.match(/entries/i):
                                return 'entries';
                            case !!cname.match(/cancel/i) && !!cname.match(/count/i) :
                                return 'cancels';
                            case !!cname.match(/cancel/i) && !!cname.match(/revenue/i) :
                                return 'cancel_value';
                            case !!cname.match(/seconds spent/i) :
                                return 'secondes';
                            default:
                                return cname;
                        }
                    });

                    let rdata = [];
                    tb.querySelectorAll('tr.hover_highlight').forEach((row,ri) => {
                        let e = {};
                        row.querySelectorAll('td').forEach((cell,ci) => {
                            let ck = cmap[ci];
                            if(!ck) return;

                            let cv = cell.textContent.trim();
                            if(!cv || cv.length<=0) cv = null;
                            if(cv && /^[\d,]+(\s*\w{2,5})?$/.test(cv))
                                cv = parseInt(cv.replace(/[^\d]/, ''));
                            e[ck] = cv;
                        });
                        rdata.push(e);
                    });
                    console.log(cmap, rdata);
                    
                    return JSON.stringify(rdata);
                })();''',
        }
    }     
    def __init__(self, mode_debug=False) :
        super().__init__('adobe', mode_debug=mode_debug)


    @staticmethod
    def __list_intro_tasks(self) :
        return worker.list_tasks(browser.__tasks__, ('login','intro'), login=worker.list_task_login_parser_params(self))

    @staticmethod
    def __list_segment_tasks() :
        return worker.list_tasks(browser.__tasks__, ('analytics', 'segments'))

    @staticmethod
    def __list_report_tasks(date) :
        def __report_parse_fn(args) :
            args['params'] = (date)
            args['post_condition'] = args['post_condition']%(date)
            return args
        return worker.list_tasks(browser.__tasks__, 
            ('report_date', 'report_data'), 
            report_date=__report_parse_fn)


    def _retrieve_report_with_window(self, sid, days) :
        for d in days :
            try :
                (date_task, data_task) = self.__list_report_tasks(d)

                timelog('set date %s'%(d))
                self.proceed_task(**date_task)

                pfs = json.loads(self.proceed_task(**data_task))            
                records = self.setmap_performance_entities(pfs)
                performance.inserts(sid, d, records)
                timelog('adobe report OK with %d records'%(len(records)))
            except Exception as ex:
                timelog('adobe report Error %s'%(str(ex)))
                traceback.print_exc()


    @staticmethod
    def setmap_performance_entities(performances) :
        keys = ('sid', 'visits','bounces','conversions','value')
        rets = []
        for pf in performances :
            if 'sid' not in pf : continue
            vals = {k:pf[k] if k in pf else None for k in keys}
            vals['stats'] = json.dumps(vals)
            rets.append(vals)
        return rets

    
    def intro(self) :
        if not self.has_account() :
            raise Exception('Account access required')
        # login and intro
        tasks = self.__list_intro_tasks(self)
        self.run_tasks(tasks)


    def retrieve_reports(self, days:tuple) :
        # load segment windows
        for sid, scode, info, title in segment.to_visits(self.service, self.login) :
            path = info['url']
            if path.startswith('/') : path = 'https://sc4.omniture.com/x%s'%(path)
            timelog('>> %s'%(path))
            # open new window
            self.driver.get(path)

            # run dates
            self._retrieve_report_with_window(sid, days)

    def retrieve_segments(self) :
        segment_tasks = self.__list_segment_tasks()
        (_,segs) = self.run_tasks(segment_tasks)
        new_segments = {s['id']:s for s in json.loads(segs)}
        segment.saves(new_segments, self.account_id)

    def process(self) :
        self.intro()
        
        time.sleep(1)

        self.retrieve_segments()

        days = [datetime.now()-timedelta(days=d) for d in range(1,7)]
        reports = tuple([d.strftime('%Y-%m-%d') for d in days])

        self.retrieve_reports(reports)

# test
if __name__ == '__main__' : 
    browser.console()
    exit(1)