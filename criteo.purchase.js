/* Local-Shop-AD(Criteo)-Purchase-ALL */
(function(url) {
    // 초기화 함수
    let __initiate = function() {
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
        return window.criteo_q;
    };
    let __resolved = function(cq) {
        let order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);
        let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
        let sitemode = 'd';
        if(order_match && basket_items) {
            let order_id = order_match[1];
            if(window.innerWidth<=1024) sitemode = 'm';
            else if(window.innerWidth<=1440) sitemode = 't';

            window.criteo_q.push([
                { event: "setAccount", account: 62197 },
                { event: "setSiteType", type: sitemode },
                { event: "trackTransaction", id: order_id, item: basket_items },
            ]);
        }
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
})('//static.criteo.net/js/ld/ld.js');