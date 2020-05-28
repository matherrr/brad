(function() {
    const mobion_id = 'pengsamsung';

    // ready for digitalData.product
    let mobion_onload = function() {
        // base script
        (function(a,g,e,n,t){a.enp=a.enp||function(){(a.enp.q=a.enp.q||[]).push(arguments)};
        n=g.createElement(e);n.defer=true;n.src=t;g.head.appendChild(n);})
        (window,document,"script",undefined,'https://cdn.megadata.co.kr/dist/prod/enp_tracker_self_hosted.min.js');
        enp('create', 'common', mobion_id, { device: 'B' });

        // prod info
        let cart_items = document.querySelectorAll('.cart-product-list .cart-item');
        let attr = function(selector, key, defaultValue, parent) {
            let el = (parent || document).querySelector(selector);
            if(el) { return el[key] || defaultValue; }
            return defaultValue;
        };

        if(cart_items && 0<cart_items.length) {
            let items = []; cart_items.forEach(function(item) {
                let id = attr('input[name="productCode"]', 'value', null, item);
                let name = attr('.name-area .name', 'textContent', null, item);
                let price = attr('.item-price', 'textContent', '', item);
                let quantity = attr('input[name="initialQuantity"]', 'value', null, item);
                if(id && name && price && quantity) {
                    items.push({
                        productCode: id,
                        productName: name,
                        price: price ? price.replace(/[^\d]+/g, '') : '0',
                        qty: quantity,
                    });
                }
            });
            window.ENP_VAR = {conversion: {product: items,}}
            enp('create', 'conversion', mobion_id, { device: 'B', paySys: 'naverPay' });
            
        } 
        else {
            let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
            let order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);

            if(basket_items && order_match) {
                let order_id = order_match[1];
                window.ENP_VAR = {
                    conversion: {
                        ordCode: order_id,
                        totalPrice: JSON.parse(window.sessionStorage.getItem('.checkout.revenue')),
                        totalQty: basket_items.reduce(function(t,i) { t += i.quantity; return t; }, 0),
                        product: basket_items.map(function(it) { return {
                                productCode: it.id,
                                productName: it.id,
                                price: it.price,
                                qty: it.quantity }}),
                    }
                }
            }
            enp('create', 'conversion', mobion_id, { device: 'B' });
            enp('send', 'conversion', mobion_id);
        }
        enp('send', 'common', mobion_id);
    }
    // run onload
    if(document.readyState.toLowerCase() == 'complete') { mobion_onload(); }
    else { window.addEventListener('load', mobion_onload); }
})();