(function(url,mode_debug) {
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
        window.ne_tgm_q = window.ne_tgm_q || [];
    }
    let __condition = function() {
        return window.ne_tgm_q;
    };
    let __resolved = function(ace) {
        let order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);
        let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
        if(order_match && basket_items) {
            let order_id = order_match[1];
            let puts = {
                tagType: 'conversion',
                device: 'web',
                uniqValue: '',
                pageEncoding: document.characterSet,
                orderNo: order_id,
                items: basket_items.map(function(item) {
                    return Object.assign({
                        category: '',
                        imgUrl: '',
                        name: '구매완료',
                        desc: '',
                        link: '',
                    }, item);
                }),
                totalPrice: JSON.parse(window.sessionStorage.getItem('.checkout.revenue'))
            }
            console.log('AceTrader', 'Purchase', puts);
            window.ne_tgm_q.push(puts);
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
})('https://static.tagmanager.toast.com/tag/view/1543');  // id값 수정