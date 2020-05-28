(function() {
    let script_url = 'https://cdn-aitg.widerplanet.com/js/wp_astg_4.0.js';
    let element_id = 'wp_tg_cts';
    let client_id = '47474';
    

    let html_element = function(tagname, attrs) {
        let el = document.createElement(tagname);
        Object.keys(attrs).forEach(function(ak) {
            el.setAttribute(ak, attrs[ak]);
        });
        return el;
    }
    let attr = function(selector, key, defaultValue) {
        let el = document.querySelector(selector);
        if(el) { return el[key] || defaultValue; }
        return defaultValue;
    };

    let wptg_push = function(attrs) {
        window.wptg_tagscript_vars = window.wptg_tagscript_vars || [];
        window.wptg_tagscript_vars.push(function() { 
            return Object.assign({
                wp_hcuid: '',
                ti:client_id,
                ty: 'Home',
                device: 'web',
            }, attrs || {})
        });
    }

    // on cart (and/or checkout)
    let cart_items = [];
    document.querySelectorAll('.cart-product-list .cart-item')
        .forEach(function(item){
        cart_items.push({
            i: attr('input[name="productCode"]', 'value', null, item),
            t: attr('.name-area .name', 'textContent', null, item),
        });
    });
    if(cart_items && 0<cart_items.length) {
        wptg_push({
            ty: 'Cart',
            items: cart_items,
        })
    } else {
        let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
        let order_match = /\/checkout\/orderConfirmation\/(?<oid>[\w-]+)/.exec(location.pathname);
        if(basket_items && order_match) {
            wptg_push({
                ty: 'PurchaseComplete',
                items: basket_items.map(function(item) {
                    return {
                        i: item.id,
                        t: item.id,
                        p: item.price,
                        q: item.quantity,
                    }
                }),
            });
        } else {
            // default (common)
            wptg_push();
        }
    }

    // initiate
    let on_load_window = function() {
        if(!document.querySelector('#'+element_id)) {
            let div_element = html_element('div', {
                id: element_id,
                style: 'display:none;'
            });
            document.body.appendChild(div_element);
        }
        // load script
        let scr_element = html_element('script', {
            type: 'text/javascript',
            src: script_url,
            async: true,
        });
        scr_element.addEventListener('load', function() {
            console.log('widerplanet ready', window.wptg_tagscript_vars);
        });
        document.head.appendChild(scr_element);
    }

    if(document.readyState.toLowerCase() == 'complete') {
        on_load_window();
    } else {
        window.addEventListener('load', on_load_window);
    }
})();