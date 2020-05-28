(function() {
    // tenping 정보 저장
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

    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };
    let append_cookie = function(key, value, options) {
        options = Object.assign(options || {}, {
            'max-age': 900,
            'domain': 'samsung.com',
            'path': '/',
        });
        document.cookie = key + '=' + value + '; ' + Object.keys(options).map((ok)=>ok +'='+ options[ok]).join('; ');
    }

    // GET 파라미터 (location.search)
    let _searches = _splitParse(location.search, /[\?&]/);
    let _cookies = _splitParse(document.cookie, /;\s*/);
    const tenping_ck = '_tenping.kr';
    const tenping_keys = ['jid','uid','cid','rd','at', 'tid', 'did', 'key'];
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
        if(!tenping_params.key) { tenping_params.key = 'scriptrequest'; }
        document.cookie = tenping_ck+'='+JSON.stringify(tenping_params)
            +';max-age=900; domain=.samsung.com;path=/';
    } 

    let tenping_conversion =  function(onloadFn) {
        let ps = _cookies[tenping_ck];
        if(!ps) return;
        _create_element('img', {
            src: 'https://api.tenping.kr/Query?' + Object.keys(ps).map((ok)=>ok+'='+ps[ok]).join('&'),
        }, document.body, onloadFn ? {'load':onloadFn} : null);
    }

    // TNK tracking
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

    /* de duplication nsmart */
    // const NSMART_TRACK_ID = 'NTA79161461';
    // let nsmart = function() {
    //     (function(c,o,n,f,u,s,e) {c['NsmartTrackingAnalytics']=f;c[f]=function(){
    //         (c[f].q=c[f].q||['MTNC', u, s]).push(arguments)};
    //         c[f].d=u,c[f].g=s,e=o.createElement(n),e.async=1,e.src=u+'/nta.js?nta_nc='+s;
    //         o.head.appendChild(e);
    //     })(window,document,'script','_NTA','//n98.nsmartta.com',NSMART_TRACK_ID);
    // }
    // let nsmart_conversion = function(ev_id) {
    //     window._NTA(ev_id, NSMART_TRACK_ID);
    // }

    // FB init
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}
    (window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
    ['147770486071750'].forEach(function(fbid) { fbq('init', fbid); });

    // gtag init
    const GDN_TRACK_ID = 'AW-805732128';
    _create_element('script', {
        async: true,
        src: 'https://www.googletagmanager.com/gtag/js?id='+GDN_TRACK_ID,
    }, document.head, null, 'script[src*="www.googletagmanager.com/gtag"]');
    window.dataLayer = window.dataLayer || [];
    let gtag = function(){ window.dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GDN_TRACK_ID);

    // after document ready
    window.addEventListener('load', function() {
        // 캠페인 메인 페이지
        if(/sec\/eventList\/bespoke_weddingshop/i.test(location.pathname)) {
            document.querySelectorAll('.btn_invitation').forEach(function(btn) {
                    btn.addEventListener('click', function() {
                    // FB on
                    fbq('track', 'ViewContent', { content_category: 'bespoke_weddingshop', content_name: 'get_invitation' });
                });
            });
        }
        // 캠페인 팝업 페이지
        else if(/comLocal\/event.*popup/i.test(location.pathname)) {
            $(document).bind('ajaxSuccess', (function(ev,jq,xhr,resp) {
                if(/comLocal\/event\/2002_bespoke\/apply/i.test(xhr.url)
                && /^0+$/.test(resp.errorFlag)) {
                    // tenping
                    tenping_conversion();
                    // nsmart 생략 (onSuccess handler 에서 처리)
                    // facebook 생략 (onSuccess handler 에서 처리)
                    // gdn
                    gtag('event', 'conversion', { send_to: 'AW-805732128/TY8BCPmIsboBEKD-mYAD' });
                    // tnk
                    tnk_conversion();
                }
            }).bind(this));
        }

    });
})();