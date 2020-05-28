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
        let sitemode = 'd';
        if(window.width<=1024) sitemode = 'm';
        else if(window.width<=1440) sitemode = 't';

        let items = [];
        document.querySelectorAll('li.cart-item').forEach(function(item) {
            try {
                let sku = item.querySelector('.cart-item-sku').textContent.trim();
                let qty = item.querySelector('input[name="quantity"]').value;
                qty = parseInt(qty);
                let price = item.querySelector('.item-price').textContent.replace(/[^\d]/g, '');
                price = parseInt(price)/qty;
                

                items.push({ id: sku, price: price, quantity: qty });
            } catch(ex) { console.log(ex); }
        });
        cq.push([
            { event: "setAccount", account: 62197 },
            { event: "setSiteType", type: sitemode },
            { event: "viewBasket", item: items },
        ]);
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