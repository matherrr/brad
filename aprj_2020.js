(function(w,d) {
    const fbids = ['721486928060510','1267833453273427'];

    // fb init
    !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
    
    
    fbids.forEach(function(fbid) {
        window.fbq('init', fbid);
    });
    // fb pageview: common
    window.fbq('track', 'PageView');

    // nsmart
    const NSMART_TID = 'NTA79653576';
    (function(c,o,n,f,u,s,e) {c['NsmartTrackingAnalytics']=f;c[f]=function(){
        (c[f].q=c[f].q||['MTNC', u, s]).push(arguments)};
        c[f].d=u,c[f].g=s,e=o.createElement(n),e.async=1,e.src=u+'/nta.js?nta_nc='+s;
        o.head.appendChild(e);
    })(window,document,'script','_NTA','//n98.nsmartta.com',NSMART_TID);
    
    // tenping push
    let _splitParse = function(s,sep,delim) {
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
    let append_cookie = function(key, value, options) {
        options = Object.assign(options || {}, common_cookie_option);
        document.cookie = key + '=' + value + '; ' + Object.keys(options).map((ok)=>ok +'='+ options[ok]).join('; ');
    }
    // GET 파라미터 (location.search)
    let _searches = _splitParse(location.search, /[\?&]/);
    let _cookies = _splitParse(document.cookie, /;\s*/);

    const tenping_ck = '_tenping.kr';
    const tenping_keys = ['jid','uid','cid','rd','at','tid','key', 'did'];
    const common_cookie_option = {
        'max-age': 900,
        'domain': 'samsung.com',
        'path': '/',
    };
    let tenping_params = tenping_keys
        .reduce(function(agg, tk) {
            if(_searches[tk]) 
                agg[tk] = _searches[tk];
            return agg;
        }, {});
    if(!(tenping_params.jid && tenping_params.uid && (tenping_params.cid || tenping_params.tid))) { tenping_params = null; }

    if(tenping_params)
        tenping_params._timestamp = Date.now();
    else if(_cookies[tenping_ck])
        tenping_params = _cookies[tenping_ck];
    // 
    if(tenping_params) {
        tenping_params.cid = tenping_params.tid || tenping_params.cid;
        tenping_params.key = tenping_params.key || 'scriptrequest';
        append_cookie(tenping_ck, JSON.stringify(tenping_params));
    }

    let tenping_conversion = (function(params) {
        if(params) {
            let el = document.querySelector('img[src*="https://api.tenping.kr/Query"]');
            if(!el) {
                el = document.createElement('img');
                el.src = 'https://api.tenping.kr/Query?'+Object.keys(tenping_params).reduce(function(tk) {
                    return tk + '=' + encodeURIComponent(tenping_params[tk]);
                }).join('&');
                document.body.appendChild(el);
            }
        }
    });

    // TNK
    const tnk_ck = '__twcc__';
    if(_searches.adkey && _searches.adkey) {
        append_cookie(tnk_ck, _searches.adkey);
    }

    let tnk_conversion = (function(event) {
        let tnk = _cookies[tnk_ck] || _searches.adkey;
        if(tnk) {
            let el = document.querySelector('script[src*="https://api3.tnkfactory.com/tnk/api/postback/script/"]');
            if(!el) {
                el = document.createElement('script');
                event = event || 'action_complete';
                el.src = 'https://api3.tnkfactory.com/tnk/api/postback/script/' + tnk + '/?event=' + event + '&callback=fn' + Date.now();
                document.head.appendChild(el);
            }
        }
    });

    // 런칭 알림
    if(/launchingalarm/.test(location.pathname)) { 
        document.querySelector('a.btn_event').addEventListener('click', function() {
            window.fbq('track', 'ViewContent', { content_category: 'notification', content_name: '런칭알림' });
        });
    }
    // 릴레이 이벤트 #엄마아빠의자유시간
    else if(/\/grande-ai\/Relayevent/.test(location.pathname)) {
        document.querySelector('.btn_tag_copy').addEventListener('click', function() {
            window.fbq('track', 'ViewContent', {content_category: 'relay_event', content_name: '해시태그'});
        });
        document.querySelector('a.btn_entry').addEventListener('click', function() {
            window.fbq('track', 'ViewContent', {content_category: 'relay_event', content_name: '릴레이팝업'});
        });
    } 
    // 매장상담 예약 이벤트 팝업
    else if(/2001_grande\/popup/i.test(location.pathname)) {
        document.querySelectorAll('button[onclick*=counselSubmit]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                let region = document.querySelector('select#local-01').value;
                let city = document.querySelector('select#local-02').value;
                let shop = document.querySelector('ul.shop-list li .on');
                let all_agreed = true; 
                document.querySelectorAll('input[type="checkbox"][id*="agree"]').forEach(function(ag) {
                    all_agreed = all_agreed && ag.checked;
                });

                if(shop && all_agreed) {
                    window.fbq('track', 'SubmitApplication', {
                        content_category: 'reservation',
                        content_name: '매장상담예약',
                        region: region,
                        city: city,
                        shop: shop.textContent.trim(),
                    });

                    // tenping CPA
                    tenping_conversion(tenping_params);
                    // tnk CPA
                    tnk_conversion();
                }
            });
        });

    }
    // 체험단 이벤트
    else if(/event\/grandeaievent/i.test(location.pathname)) {
        document.querySelector('.btnHashTag').addEventListener('click', function() {
            window.fbq('track', 'ViewContent', {content_category: 'grande_event', content_name: '해시태그'});
        });
        document.querySelector('.btnJoin').addEventListener('click', function() {
            window.fbq('track', 'ViewContent', {content_category: 'grande_event', content_name: '체험단팝업'});
        });
    }

})(window,document);