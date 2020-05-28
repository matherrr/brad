(function() {
    const tnk_ck = '__twcc__';
    const tnk_chk = '__twcc2__';
    const GID = 'UA-159340113-1';
    const CAMPAIGN = 'dishwasher_2020';

    let import_script = function(u,o) {
        if(document.querySelector('script[src*="'+u+'"]')) {
            if(o) o();
            return document.querySelector('script[src*="'+u+'"]');
        }
        let se = document.createElement('script');
        let at = {async: true, type: 'text/javascript', src: u};
        Object.keys(at).forEach(function(ak) {
            se[ak] = at[ak];
        });
        if(o)
            se.addEventListener('load',o);
        document.head.appendChild(se);
        return se;
    }
    let save_cookie = function(key, value) {
        if(!value) return;
        document.cookie = key + '=' + value
            + ';max-age=900;domain=.samsung.com;path=/';
    }

    if(!window.dataLayer) { window.dataLayer = []; }
    if(!window.gtag) {
        window.gtag = function() { window.dataLayer.push(arguments); };
        window.gtag('js', new Date());
    }
    import_script('https://www.googletagmanager.com/gtag/js');

    let pv = function(path_suffix, source, medium, content) {
        if(window.gtag) {
            let path = '/dishwasher/' + path_suffix;
            let utms = (source && medium) ? {
                campaign: CAMPAIGN,
                source: source,
                medium: medium,
                content: content,
            } : {};

            gtag('config', GID, {
                page_path: path,
                page_location: 'https://www.samsung.com' + path
                    + '?' + Object.keys(utms)
                        .map((uk) => 'utm_'+uk+'='+encodeURIComponent(utms[uk])).join('&'),
            });
        }
    }

    let cpa = function(channel, label) {
        if(window.gtag) {
            gtag('event', 'cpa', {
                event_category: channel,
                event_label: label,
                send_to: GID,
            });
        }
    }

    let split_parse= function(s,sep,delim) {
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
    }
    let _cookies = split_parse(document.cookie, /;\s*/);
    let _searches = split_parse(location.search, /[\?&]/);
    let proceed;

    // 캠페인 메인
    if(/\/eventList\/2020dishwashers\/launching/i.test(location.pathname)) {
        proceed = function() {
            if(_searches.adkey) {
                pv('main', 'cpa', 'tnk', _searches.adkey);
                save_cookie(tnk_ck, _searches.adkey, 900);
                if(_searches.chkey) {
                    save_cookie(tnk_chk, _searches.chkey);
                }
            } else if(_cookies[tnk_ck]) {
                save_cookie(tnk_ck, _cookies[tnk_ck]);
                if(_cookies[tnk_chk]) {
                    save_cookie(tnk_chk, _cookies[tnk_chk]);
                }
            }
        }
    }
    // 매장 상담 팝업의 TNK submit
    else if(/local\.sec\./i.test(location.hostname) && /\/2004_dishwash\/popup\./i.test(location.pathname)) {
        proceed = function() {
            if(_cookies[tnk_ck]) {
                pv('popup', 'cpa', 'tnk', _cookies[tnk_ck]);
                save_cookie(tnk_ck, _cookies[tnk_ck]);
                if(_cookies[tnk_chk]) {
                    save_cookie(tnk_chk, _cookies[tnk_chk]);
                }
            }
            // add event listener
            let validation = function() {
                let required_inputs = {
                    'input#userNm': null,
                    'select#userPhone1': null,
                    'input#userPhone2': null,
                    'input#userPhone3': null,
                    'li.shop-list_button': (v,input) => v || input.classList.contains('on'),
                    'input#agree1': (v,input) => input.checked,
                    'input#agree2': (v,input) => input.checked,
                    'input#agree3': (v,input) => input.checked,
                }
                return Object.keys(required_inputs).reduce((pass, selector) => {
                    if(!pass) return false;
    
                    let ctrls = [];
                    document.querySelectorAll(selector).forEach((c)=> { ctrls.push(c); });
                    if(required_inputs[selector])
                        return ctrls.reduce(required_inputs[selector], true);
                    else 
                        return ctrls.reduce((v,o)=>v || !!o.value, true);
                }, true);
            }
            document.querySelector('button.reservation_button').addEventListener('click', function() {
                // check inputs
                if(validation()) {
                    cpa('tnk', _cookies[tnk_ck]);
                    import_script('https://api3.tnkfactory.com/tnk/api/postback/script/'
                        + _cookies[tnk_ck] + '/?event=action_complete&callback=fn' + Date.now());
                }
            });
        }
    } 

    if(proceed) {
        if(document.readyState=='complete') proceed();
        else {
            window.addEventListener('load', proceed);
        }
    }
})();