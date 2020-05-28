(function() {
    // constants
    const GID = 'UA-159340113-1';
    const UTM_CAMPAIGN_DEFAULT = 'e_return.2020';
    const TRACK_IDS = {
        google: [],
        facebook: ['211169836140452', '1040731766101815'],
        nsmart: 'NTA84931725',
        crosstarget: '5e05a4b1f1c49a8f128b4567',
    }

    const urls = {
        gtag: 'https://www.googletagmanager.com/gtag/js',
        nsmart: 'https://n98.nsmartta.com/nta.js?nta_nc=' + TRACK_IDS.nsmart,
        tnk: 'https://api3.tnkfactory.com/tnk/api/postback/script/',
        tenping: 'https://api.tenping.kr/Query?',
        crosstarget: 'https://st2.exelbid.com/js/cts.js',

    }

    const tenping_ck='_tenping.kr';
    const tnk_ck = '__twcc__';
    const tnk_chk = '__twcc2__';


    // utils
    let split_parse = function(s,sep,delim) {
        let separator = sep || '&';
        let delimiter = delim || '=';
        return s.split(separator).reduce(function(agg,t) {
            if(t && 0<t.length) {
                let ts = t.split(delimiter);
                let k = ts && 0<ts.length ? ts[0].toString() : null;
                let v = ts && 1<ts.length ? ts[1] : undefined;
                try { v = JSON.parse(v);} catch(ex) {}
                agg[k] = v;
            }
            return agg;
        }, {});
    };
    let html_element = function(tagname, attrs, appendTo, onLoad) {
        let se = document.createElement(tagname);
        Object.keys(attrs).forEach(function(ak) {
            se[ak] = attrs[ak];
        });
        se.addEventListener('load', onLoad);
        appendTo.appendChild(se);
    };
    let import_script = function(u,o) {
        html_element('script', {async: true, type: 'text/javascript', src: u}, document.head, o);
    };
    let send_pixel = function(u,d,o) {
        if(!(d && document.querySelector('#'+d)))
            html_element('img', {id: d, src: u}, document.body, o);
    };
    let save_cookie = function(key, value, expires, domain, path) {
        if(!value) return;
        document.cookie = key + '=' + value
            + (expires ? ';max-age=' + expires : '')
            + (domain ? ';domain=' + domain : '')
            + (path ? ';path=' + path : '');
    }

    let log_pageview = function(path) {
        if(!window.gtag) return;

        window.gtag('config', GID, {
            page_path: path,
            page_location: 'https://www.samsung.com'  + path + 
                (utms ? '?' + Object.keys(utms).map((uk)=>'utm_'+uk+'='+utms[uk]).join('&') : ''),
        });
    }

    let log_conversion = function(channel, label) {
        if(!window.gtag) return;

        window.gtag('event', 'cpa', {
            event_category: channel,
            event_label: label,
            send_to: GID,
        });
    }

    let __cookies = split_parse(document.cookie, /;\s*/);
    let __searches = split_parse(location.search, /[\?&]/);

    // save cookies
    // TNK
    let tnk_searches = {adkey: tnk_ck, chkey: tnk_chk};
    Object.keys(tnk_searches).forEach(function(sq) {
        if(__searches[sq])
            save_cookie(tnk_searches[sq], __searches[sq], 900, '.samsung.com', '/');
    });

    // tenping
    let tenpings = ['jid','uid','cid','rd','at','tid','key'].reduce(function(agg, tk) {
        agg[tk] = __searches[tk];
        return agg;
    }, {});
    // tid 값이 들어온 경우
    if(tenpings.tid) { tenpings.cid = tenpings.tid, delete tenpings.tid; }
    // 쿠키 정보가 들어온 경우 덮어쓰기
    if(!(__searches.jid && __searches.uid) && __cookies[tenping_ck]) { tenpings = __cookies[tenping_ck]; }
    // 유효성 확인
    if(!(tenpings.jid && tenpings.uid && tenpings.cid)) { 
        delete tenpings; 
        tenpings = undefined;
    } else {
        save_cookie(tenping_ck, JSON.stringify(tenpings), 900, '.samsung.com', '/');
    }

    // CID to UTM
    let utms;
    let assign_utms = function(campaign, source, medium, content, term) {
        if(!utms) utms = {};

        // required
        utms.campaign = utms.campaign || campaign;
        utms.source = source;
        utms.medium = medium;

        // optional
        if(content) utms.content = content;
        if(term) utms.term = term;

        return utms;
    }
    // 
    if(__searches.utm_campaign) {
        utms = ['campaign','source','medium','content','term'].reduce(function(gg, uk) {
            if(__searches['utm_'+uk]) gg[uk] = __searches['utm_'+uk];
            return gg;
        }, {});
    } 
    else if(__searches.cid && typeof(__searches.cid)=='string') {
        let ctoks = __searches.cid.split('_');
        if(9<=ctoks.length) {
            assign_utms(ctoks[6] || UTM_CAMPAIGN_DEFAULT, ctoks[1], ctoks[3], ctoks[8], 10<=ctoks.length ? ctoks[9] : null);
        }
    }

    // gtag
    let gtag_init = function() {
        let on_load = function() {
            TRACK_IDS.google.forEach((gid) => { window.gtag('config', gid); });
        }

        if(!window.gtag) { 
            window.dataLayer = window.dataLayer || [];
            gtag = window.gtag || function() { window.dataLayer.push(arguments); };
            gtag('js', new Date());
            // import_script
            import_script(urls.gtag, on_load);
        }
        else { on_load(); }
    }

    let gtag_event = function(category, action, params) {
        let prs = Object.assign(params, { event_category: category });
        window.gtag('event', action, prs);
    }

    // NSmart
    let nsmart_init = function() {
        window.NsmartTrackingAnalytics = '_NTA';
        window._NTA = function() { window._NTA.q = (window._NTA.q || []); window._NTA.q.push(arguments)};
        window._NTA.d = 'https://n98.nsmartta.com';
        window._NTA.g = TRACK_IDS.nsmart;
        import_script(urls.nsmart);
    }

    let nsmart_conversion = function(ev) { window._NTA.EVT(ev); }

    // Facebook
    let fb_init = function() {
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
        TRACK_IDS.facebook.forEach(function(fbid){ window.fbq('init', fbid) });

        window.fbq('track', 'PageView');
    }
    let fb_conversion = function(ev, params) { window.fbq('track', ev, params);  }

    // TNK
    let tnk_conversion = function(ev) { 
        let tnk = __searches.adkey || __cookies[tnk_ck];
        if(tnk) {
            log_conversion('tnk', ev);
            import_script(urls.tnk + tnk + '/?event=' + ev + '&callback=fn' + Date.now());

            // utms
            assign_utms(UTM_CAMPAIGN_DEFAULT, 'cpa', 'tnk');
        }
    }
    
    // tenping
    let tenping_conversion = function() {
        // 필수값 확인
        if(!(tenpings && tenpings.jid && tenpings.uid && tenpings.cid)) { 
            delete tenpings; 
            tenpings = undefined;
        }
        
        if(tenpings) {
            log_conversion('tenping', tenpings.jid);
            let prs = Object.keys(tenpings)
                .map((ok)=>ok + '=' + tenpings[ok]).join('&');
            send_pixel(urls.tenping + prs);

            // utms
            assign_utms(UTM_CAMPAIGN_DEFAULT, 'cpa', 'tenping');
        }
    }

    // CrossTarget
    let crosstarget_init = function() {
        window.ex2cts = window.ex2cts || {cmd:[]};
        window.ex2cts.push = window.ex2cts.push || (function() {
            if(this.callFunc) this.callFunc.apply(this, arguments);
            else this.cmd.push(arguments);
        }).bind(window.ex2cts);
        if(!document.querySelector('script[src*="'+urls.crosstarget+'"]')) {
            import_script(urls.crosstarget);
        }
        window.ex2cts.push('init', TRACK_IDS.crosstarget);

        //  utms
        // assign_utms(UTM_CAMPAIGN_DEFAULT, 'cpa', 'crosstarget');
    }

    let crosstarget_conversion = function(ev) { window.ex2cts.push('track', ev); }

    let preset_events = function(events) {
        events.forEach(function(track) {
            (document.querySelectorAll(track.selector) || []).forEach(function(el) {
                el.addEventListener(track.event, function() {
                    //
                    if(!(track.no_duplicate && track.hit)) {
                        track.hit = track.hit ? track.hit + 1 : 1;
                        window.gtag('event', event.act, {
                            event_category: track.category,
                            event_label: track.label,
                            non_interaction: true
                        });
                        window.fbq('track', 'ViewContent', {
                            content_category: track.category,
                            content_type: track.act,
                            content_name: track.label,
                        });
                    }
                });
            });
        });
    }

    // 캠페인 메인 페이지 스크립트
    let on_campaign_main = function() {
        log_pageview('/e_return');

        preset_events([
            // 이벤트1: 바나나우유 당첨 이벤트
            // 힌트보기
            {selector: '.btn-layer-hint', event: 'click', category: 'event01', act: 'details', label: 'hint', no_duplicate: true },
            // 정답확인
            {selector: '.btn-answer', event: 'submit', category: 'event01', act: 'submit', label: 'check', no_duplicate: true, interactive: true },

            // 복권클릭
            {selector: '.btn-scratch', event: 'check', category: 'event01', act: 'apply', label: 'apply'},
            // 당첨확인
            {selector: '.event01-section .quiz .result .correct a.btn-event', event: 'confirm', category: 'event01', act: 'confirm', label: 'gift', no_duplicate: true },

            // 이벤트2: 행사제품 더보기
            {selector: '.event02-section .btn-pd-more', event: 'click', category: 'event02', act: 'more', label: 'products', no_duplicate: true },

            // 이벤트3: 환급신청
            {selector: '.event03-section .acco-btn-list a', event: 'click', category: 'event03', act: 'details', label: 'registration', no_duplicate: true},

            // 이벤트3: 행사제품 더보기
            {selector: '.event03-section .recommand-prod .btn-list-more', event: 'click', category: 'event03', act: 'more', label: 'products', no_duplicate: true},

            // 이벤트3: 환금신청 링크 클릭
            {selector: 'a[href*="rebate.energy.or.kr"]', event: 'click', category: 'event03', act: 'apply', label: 'registration'},
        ]);

        // 이벤트2: 페이스북 버튼 전환
        document.querySelectorAll('.event02-section a.btn-link').forEach(function(ln) {
            ln.addEventListener('click', function() {
                fb_conversion('EnergyreturnO2OEvent1');
            });
        });
        
    }

    // 초대장 받기 스크립트
    let on_campaign_invitation_validation = function() {
        let validations = {
            'input[name="userNm"]': function(v, c) { return /.+/u.test(c.value) },
            'input[type="tel"]': function(v, c)  { return v && /\d+/.test(c.value) },
            'input[name="memNo"]': function(v, c) { return /.+/.test(c.value) },
            //'input[type="checkbox"][name="prod"]': function(v, c, ci) {  return (0<=ci ? v : false) || c.checked; },
            'input#agree1': function(v, c) { return c.checked },
            'input#agree2': function(v, c) { return c.checked },
            'input#agree3': function(v, c) { return c.checked },
            //'input#agree4': function(v, c) { return c.checked },  // 추가 됨
        }

        return Object.keys(validations).reduce(function(v, sel) {
            if(!v) return false;

            let validator = validations[sel];
            let elements = [];
            document.querySelectorAll(sel).forEach(function(el) {
                elements.push(el);
            });
            let rs = elements.reduce(validator, v);
            return rs;
        }, true);
    }

    let on_campaign_invitation_validation_1 = function(){
        let elements = [];
        document.querySelectorAll('input[type="checkbox"][name="prod"]').forEach(function(el) {
                    elements.push(el.checked);
                });
        let rs = elements.includes(true);
        
        //window.console.log(rs)
        return rs
    }

    let on_campaign_invitation = function() {
        log_pageview('/e_return/pop');
        
        //document.querySelectorAll('.reservation_button').forEach(function(btn) {
        document.querySelectorAll('.reservation_button').forEach(function(btn) {    
            btn.addEventListener('click', function() {
                if(on_campaign_invitation_validation() && on_campaign_invitation_validation_1() ){
                    tenping_conversion();
                    tnk_conversion('action_complete');
                    nsmart_conversion(2065);
                    
                } 
                else{
                //gtag_event('event02', 'submit', { non_interaction: true });
                    return ;
                // crosstarget_conversion('e_r_invite');
                }
            });
        });
        console.log('invitation ready');
    }

    // location on load
    let __initiated = false;
    let __main__ = (function() {
        if(__initiated) return; 
        __initiated = true;
        // init pixels
        gtag_init();
        nsmart_init();
        fb_init();
        // tenping, tnk skip
        crosstarget_init();

        // location 판별:
        switch(true) {
            // campaign main
            case /www\./i.test(location.hostname) && /sec\/eventList\/onoff_energyreturn/i.test(location.pathname) :
                on_campaign_main();
                break;

            // invitation
            case /local\./i.test(location.hostname) && /event\/membership\/2005_onoff\/popup\./i.test(location.pathname) :
                // 
                on_campaign_invitation();
                break;
        }
    });

    window.addEventListener('load', __main__);
    // __main__();
})();