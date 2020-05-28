/*
    MediaMath Universal Tag Scripts for SEC website
    @v1.0 May.12. 2020. yg1.song@cheilpengtai, adtech / Pengtai Korea
*/
(function() {
    // 
    const mediamath_img_path = 'https://pixel.mathtag.com/event/img';
    // refer: https://mediamathsupport.force.com/s/contentdocument/0692I000005JXESQA4
    const mediamath_default_attrs = {
        mt_adid: '237740',  // client account ID
        // mt_id: null,        // pixel ID
        mt_exem: '',        // Hashed email. No you can't have. Legal issue presented.
        mt_excl: '',        // Hashed LoginID. Ditto.

        // defaults
        document_title: document.title,
        previous_url: document.referrer, 
        location: window.location.href,
        host: window.location.hostname,
        path: window.location.pathname, 
        search_query: window.location.search,
        
        /* optional parameter maps
        *

        channel: '', // marketing channel type. may retrieved from CID.
        currency: 'KRW',
        delimiter: '|', // multiple value delimiter, i.e. delimiter=,&product_id=1,2,3
        
        // checkout & purchase
        order_id: '',
        product_id: '',
        product_name: '',
        product_price: '',
        product_quantity: '',
        product_category: '',
        product_category_id: '',
        product_discount_price: '',
        product_color: '',
        product_rating: '',
        product_status: '', // 'in stock' | 'out of stock'

        product_quantity_sum: '',

        revenue: '',

        // and others
        v1: '',v2: '',v3: '',v4: '',v5: '',v6: '',v7: '',v8: '',v9: '',v10: '',
        s1: '',s2: '',s3: '',s4: '',s5: '',s6: '',s7: '',s8: '',s9: '',s10: '',
        */
    }

    const mediamath_pixel = {
        pageview:    '1478782',
        // index:       '1478783',
        // category:    '1479161',
        // item_detail: '1479162',
        cart:        '1479163',
        checkout:    '1479173',
        purchase:    '1479176',
        add_cart:    '1479177',
        add_wish:    '1479178',
    }

    var mm_pixel = function(pixel_id, attrs, duplication_selector) {
        // duplication selector presented & contains duplication.
        // stop the procedure
        if(duplication_selector && !!document.querySelector(duplication_selector)) { return; }

        var px_attrs = Object.assign({mt_id: pixel_id}, mediamath_default_attrs, attrs);
        var px_path = mediamath_img_path + '?' + Object.keys(px_attrs)
            .filter(function(pk){ return px_attrs[pk]!=null; })
            .map(function(pk) {
                return pk + '=' + encodeURIComponent(px_attrs[pk]);
            })
            .join('&');
        
        var px = document.createElement('img');
        px.width=1;px.height=1;px.src = px_path;
        // diplay hide on load complete
        px.addEventListener('load', function() { px.style="width: 0px; height: 0px; display: none;" });
        // append to the container
        document.body.appendChild(px);
    }

    var try_pagepath = function(pattern) {
        return function() {
            try {
                return pattern.test(location.pathname);
            } catch(ex) {
                return false;
            }
        }
    }

    var text_to_int = function(text)  {
        try {
            return parseInt(text.replace(/[^\d]/g, ''));
        } catch(ex) {
            return Number.NaN;
        }
    }

    var element_text = function(selector, base) {
        var el = (base || document).querySelector(selector);
        return !!el ? el.textContent : null;
    }
    var element_attr = function(selector, attribute, base) {
        var el = (base || document).querySelector(selector);
        return !!el ? el[attribute] : null;
    }

    // default "pageview"
    mm_pixel(mediamath_pixel.pageview, null, 'img[src*="'+'"][src*="mt_id='+mediamath_pixel.pageview+'"]');

    const sec_pixel_mapper = [
        /* 
            Order by mapping priority -

            px: pixel ID,
            v: validate function. return "True" on valid condition.
            a: attribute function. return parameter object for the pixel.
            d: duplication selector
        */
        // Conversion (Purchase/order complete)
        {   px: mediamath_pixel.purchase,  
            v: try_pagepath(/\/checkout\/orderConfirmation\/([\w-]+)/i), 
            a: function() {
                // order information
                let order_id = /\/checkout\/orderConfirmation\/(?<oid>[\w-]+)/.exec(location.pathname).groups.oid;
                let items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
                let revenue = JSON.parse(window.sessionStorage.getItem('.checkout.revenue'));
                let delim = ',';

                return {
                    order_id: order_id,
                    product_id: items.map(function(i) { return i.id }).join(delim),
                    product_price: items.map(function(i){ return i.price.toString() }).join(delim),
                    product_quantity: items.map(function(i) { return i.quantity.toString() }).join(delim),
                    currency: 'KRW',
                    delimiter: delim,
                    revenue: revenue,
                }
            } 
        },
        // cart
        {   px: mediamath_pixel.cart, 
            v: try_pagepath(/\/sec\/cart\/?/i),
            a: function() { 
                var delim = ',';
                var items = [];
                document.querySelectorAll('.cart-product-list li.cart-item').forEach(function(t) {
                    items.push({
                        id: element_attr('input[name="productCode"]', 'value', t),
                        name: element_text('.cart-item-details .name-area > a', t),
                        price: text_to_int(element_text('.item-price'), t),
                        quantity: text_to_int(element_attr('input[name="initialQuantity"]', 'value', t)),
                    });
                });
                return {
                    product_id: items.map(function(item){ return item.id.replace(delim, '') }).join(delim),
                    product_name: items.map(function(item){ return item.name.replace(delim, '') }).join(delim),
                    product_price: items.map(function(item){ return item.price.toString() }).join(delim),
                    product_quantity: items.map(function(item){ return item.quantity.toString() }).join(delim),
                    delimiter: delim,
                    revenue: text_to_int(element_text('.cart-totals .totals')),
                }
            } 
        },
        // checkout
        {   px: mediamath_pixel.checkout, 
            v: try_pagepath(/\/sec\/checkout\//i),  
            a: function() { 
                let items = [];
                document.querySelectorAll('ul.checkout-order-summary-list li.checkout-order-summary-list-items').forEach(function(t) {
                    items.push({
                        id: element_text('.details .code', t),
                        name: element_text('.details .name', t).replace(/\s{2,}/g, ' '),
                        price: text_to_int(element_text('.details .product-price', t)),
                        quantity: text_to_int(element_text('.details .product-classifications', t)),
                    });
                });
                let delim = ',';

                return {
                    product_id: items.map(function(i) { return i.id }).join(delim),
                    product_name: items.map(function(item){ return item.name.replace(delim, '') }).join(delim),
                    product_price: items.map(function(i){ return i.price.toString() }).join(delim),
                    product_quantity: items.map(function(i) { return i.quantity.toString() }).join(delim),
                    currency: 'KRW',
                    delimiter: delim,
                    revenue: document.querySelector('.checkout-order-summary .subtotals').dataset.price,
                }
            }
        },
    ];

    // RUN THE Pixel Mapper
    var mm_onload = function()  {
        var proc = null;
        sec_pixel_mapper.forEach(function(mapp) {
            if(!proc && mapp.v && mapp.v()) proc = mapp;
        });
        // procedure has set
        if(proc) {
            var pattrs = proc.a ? proc.a() : {};
            var pdups = proc.d ? proc.d() : undefined;
            // run the pixel
            mm_pixel(proc.px, pattrs, pdups);
        }
    }

    // if document has set, run directly
    if(document.readyState == 'complete') { mm_onload();} 
    // or wait for the DOM ready
    else { window.addEventListener('load', mm_onload); }

})();