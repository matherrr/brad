(function(url) {
    const client_id = 'ttdUniversalPixelTag92c5418d439f4bf1b9d7ad53873e94d6'
    // 초기화 함수
    let __initiate = function() {
        if(!document.querySelector('#'+client_id)) {
            let ttd = document.createElement('div');
            ttd.style = 'display:none;'
            ttd.id = client_id;
            document.body.appendChild(ttd);
        }
        if(!document.querySelector('script[src*="'+url+'"]')) {
            let se = document.createElement('script');
            se.async = true;
            se.src = url;
            se.type = 'text/javascript';
            se.async = true;
            document.head.appendChild(se);
        }

    }
    let __condition = function() {
        if(window.TTDUniversalPixelApi && typeof window.TTDUniversalPixelApi == 'function')
            return window.TTDUniversalPixelApi;
        else
            return null;
    };
    let __resolved = function(ttd) {
        let ttd_api = new TTDUniversalPixelApi();
        ttd_api.init('w473oq0', ['6vqxi3m'], 'https://insight.adsrvr.org/track/up', client_id);
        ttd_api.init('pf35t7n', ['8yhnu4y'], 'https://insight.adsrvr.org/track/up', client_id);
    };
    let resolve = function(rs) {
        if(__interval) clearInterval(__interval);
        try {
            __resolved(rs);
        } catch(ex) { /* silence! */ }
    }

    __initiate();
    let __interval = setInterval(function() {
        let rs = __condition();
        return rs ? resolve(rs) : null;
    }, 1);
})('https://js.adsrvr.org/up_loader.1.1.0.js');