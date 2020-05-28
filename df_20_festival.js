(function() {
    const tenping_ck = '_tenping.kr';

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
    }

    // searches
    let _searches = _splitParse(location.search, /[\?\&]/);
    let _cookies = _splitParse(document.cookie, /;\s*/);


    // conversion
    let conversion_track = (function(selector, event, handler, has_load_complete) {
        let __intervals = setInterval(function() {
            if(has_load_complete && !has_load_complete()) return;
            let elems = document.querySelectorAll(selector);
            if(!elems || elems.length <=0)  return;

            clearInterval(__intervals);
            elems.forEach(function(element) {
                element.addEventListener(event, handler);
            });

        }, 50);
    });


    // campaign popup
    if(/\/popup\./i.test(location.pathname)) {
        let tenping_params = _cookies[tenping_ck];
        let furfilled = (function() {
            let pass = true;
            // 필수 입력
            ['userNm', 'userPhone1', 'userPhone2', 'userPhone3'].forEach(function(iid) {
                pass = pass &&  !!document.querySelector('#'+iid).value;
            });
            if(!pass) return false;
            
            // 최소 1개
            pass = false;
            document.querySelectorAll('input[type="checkbox"][name="prod"]').forEach(function(p) {
                if(p.checked) pass = true;
            });
            if(!pass) return false;

            pass = true;
            document.querySelectorAll('input[type="checkbox"][name="terms"]').forEach(function(p, pi) {
                if(pi<3 && !p.checked) pass = false;
            });
            if(!pass) return false;

            return true;
        });

        let submit_conversion = (function(ev) {
            if(!furfilled() || !tenping_params) return;
            if(!document.querySelector('img[src*="tenping.kr/Query"]')) {
                let px = document.createElement('img');
                tenping_params = Object.assign(tenping_params, {key: 'scriptrequest'});
                px.src='http://api.tenping.kr/Query?' + Object.keys(tenping_params)
                    .map((ok) => ok+'='+encodeURIComponent(tenping_params[ok]))
                    .join('&');
                document.body.appendChild(px);
            }
        });

        conversion_track('button.reservation_button', 'click', submit_conversion);
    }
    else {
        let tenping_params = Object.keys(_searches)
            .filter(function(k) { return 0<=['jid','uid','cid','rd','at','did'].indexOf(k)})
            .reduce(function(g,k) { g[k] = _searches[k]; return g; }, {});

        if(tenping_params && 0<Object.keys(tenping_params).length) {
            let cv = tenping_ck + '=' + JSON.stringify(tenping_params)
            + ';max-age=900;domain=samsung.com;path=/';
            document.cookie = cv;
        }
        let btn_conversion = (function(ev) {
            if(window.gtag) {
                window.gtag('event', 'conversion', { send_to: 'AW-805732128/wejECI7tpbgBEKD-mYAD' });
            }
            if(window.fbq) {
                window.fbq('track', 'DigitalPlaza20sEvent1');
            }
        });

        // button click on
        conversion_track('.btn_event', 'click', btn_conversion);
        conversion_track('.btn-invitation', 'click', btn_conversion);
    }
})();