(function() {
    let __initiate = function() {
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '211169836140452');
        fbq('init', '1040731766101815');
    }
    let __condition = function() {
        return window.fbq;
    };
    let __resolved = function(fbq) {
        let items = [];
        let total_price = 0;
        document.querySelectorAll('.cart-product-list li.cart-item')
            .forEach(function(item) {
                try {
                    let qty = parseInt(item.querySelector('input[name="quantity"]').value);
                    let price = parseInt(item.querySelector('.item-price').textContent.sub(/[^\d]/g, '')) || 1;
                    total_price += price;
                    if(1<qty) 
                        price = Math.round(price/qty);

                    items.push({
                        id: item.querySelector('input[name="productCode"]').value.trim(),
                        quantity: qty,
                        price: price,
                    });
                } catch(ex) {}
            });
        fbq('track', 'AddToCart', {
            content_ids: items.map(function(i){ return i.id; }),
            content_name: 'Shopping Cart',
            value: total_price || 1,
            contents: items,
            currency: 'KRW',
            content_type: 'product'
        });       
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
})();