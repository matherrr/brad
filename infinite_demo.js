(function() {
 
    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };

    // FB init
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}
    (window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
    ['211169836140452'].forEach(function(fbid) { fbq('init', fbid); });
    
    window.fbq('track', 'PageView');

    // gtag init 
    const GDN_TRACK_ID = 'AW-805732128';
    _create_element('script', {
        async: true,
        src: 'https://www.googletagmanager.com/gtag/js?id='+GDN_TRACK_ID,
    }, document.head, null, 'script[src*="www.googletagmanager.com/gtag"]');
    if(!window.dataLayer) {
        window.dataLayer = [];
    }
    if(!window.gtag){
        window.gtag = function() { window.dataLayer.push(arguments); }
        gtag('js', new Date());
    };
    gtag('config', GDN_TRACK_ID);

    // MediaMath 
    let loading_mediamath = (function(){
    const MediaMath_Track_ID = '1467346';
    _create_element('script', {
        async: true, 
        src: '//pixel.mathtag.com/event/js?mt_id='+MediaMath_Track_ID+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3=',
    }, document.head, null, 'script[src*="//pixel.mathtag.com/event/"]');
    });

    // TTD loading
    let loading_ttd = (function(){
        _create_element('script', {
            async: true,    // 비동기로 실행되는 어싱크가 있으므로 밑에 ttd_pixel이 안잡혔던거였다
            type: "text/javascript",
            src: 'https://js.adsrvr.org/up_loader.1.1.0.js',
        }, document.head, null);
    });
    // 윗윗줄에 null 자리에 ttd_pixel 함수 넣으면 리스너로 로딩티티디가 끝나면 티티디픽셀이 돌아가게 끔 되는거임

    let ttd_pixel = (function() {
        if (typeof TTDUniversalPixelApi === 'function') {
            let universalPixelApi = new TTDUniversalPixelApi();
            universalPixelApi.init("9hr56de", ["vfqqhh5"], "https://insight.adsrvr.org/track/up");
        }
    });
/*
    let tenping_conversion =  function(onloadFn) {
        let ps = _cookies[tenping_ck];
        if(!ps) return;
        _create_element('img', {
            src: 'https://api.tenping.kr/Query?' + Object.keys(ps).map((ok)=>ok+'='+ps[ok]).join('&'),
        }, document.body, onloadFn ? {'load':onloadFn} : null);
    }

    let loading_ttd = (function(){
    _create_element('script', {
        async: true,    // 비동기로 실행되는 어싱크가 있으므로 밑에 ttd_pixel이 안잡혔던거였다
        type: "text/javascript",
        src: 'https://js.adsrvr.org/up_loader.1.1.0.js',
    }, document.head, ttd_pixel ? {'load':ttd_pixel}: null);
});


*/

    //Tenping
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
        options = Object.assign(options || {}, {
            'max-age': 1800,    //쿠키 값 30분 유지
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
            +';max-age=1800; domain=.samsung.com;path=/';
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
        append_cookie(tnk_ck, _searches.adkey);  /* 쿠키값 기본 30분 설정*/
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

    // Buzz vill trancking   max age 30분으로 설정
    const Buzz_ck = 'BuzzAd';
    if(_searches.bz_tracking_id && _searches.bz_tracking_id) {
        append_cookie(Buzz_ck, _searches.bz_tracking_id);
    }

    let BuzzVill_conversion = (function(){
        let buzz = _cookies[Buzz_ck] || _searches.bz_tracking_id
        if(buzz) {
            // _create_element 로 바꾸기
            let el = document.querySelector('img[src*="https://track.buzzvil.com/action/pb/cpa/default/"]');
            if(!el) {
                el = document.createElement('img');
                el.src = 'https://track.buzzvil.com/action/pb/cpa/default/?'+bz_tracking_id+'='+buzz;
                document.head.appendChild(el);
            }
        }
    } ); 

    // 클릭 건에 대해 텐핑, TNK, 버즈빌만 필요
    // after document ready 
    if(/comLocal\/event\/qled8k/i.test(location.pathname)) {
        window.addEventListener('load', function() {
            // ttd, mediamath, facebook, google 로딩
            //fbq('track', 'pageView'); 맨위로 뺌
            ttd_pixel();
            loading_mediamath();

            // 성과형 (텐핑, TNK, 버즈빌)
            // 성과형은 제대로 신호가갔는지에 대한 확답을 받은후 리스너를 달기 (페이지 나와야 확정남)
            if(/comLocal\/event\/qled8k/i.test(location.pathname)) {
                document.querySelectorAll('.blue_button').forEach(function(btn) {
                        btn.addEventListener('click', function() {
                        //tenping
                        tenping_conversion();
                        //tnk
                        tnk_conversion();
                        //buzz
                        BuzzVill_conversion();
                    
                    });
                });
            };

        });
    };
})();