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

        product_price_total: '',
        product_quantity_sum: '',

        revenue: '',

        // and others
        v1: '',v2: '',v3: '',v4: '',v5: '',v6: '',v7: '',v8: '',v9: '',v10: '',
        s1: '',s2: '',s3: '',s4: '',s5: '',s6: '',s7: '',s8: '',s9: '',s10: '',
        */

    }

    const mediamath_pixel = {
        pageview:    '1478782',
        index:       '1478783',
        category:    '1479161',
        item_detail: '1479162',
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
        // tester instead
    }

    var try_pagetrack = function(pattern) {
        return function() {
            try {
                return pattern.test(digitalData.page.pageInfo.pageTrack.trim());
            } catch {
                return false;
            }
        }
    }

    var text_to_int = function(text)  {
        try {
            return parseInt(text.replace(/[^\d]/g, ''));
        } catch {
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
        // home
        {   px: mediamath_pixel.index,  
            v: try_pagetrack(/^home$/i), 
            a: undefined },
        // category (product list)
        {   px: mediamath_pixel.category, 
            v: try_pagetrack(/product finder$/i),
            a: function() { 
                var item_delimiter = ',';
                var items = [];
                document.querySelectorAll('.product-card').forEach(function(t) {
                    items.push({
                        id: element_text('.product-card__prd-info-title-serial', t).trim(),
                        name: element_text('.product-card__prd-info-title-name', t).trim(),
                    });
                });
                return {
                    product_category: element_attr('input#pfcategoryLocalTitle', 'value'),
                    product_category_id: element_attr('input#categoryTypeCode', 'value'),
                    product_id: items.map(function(item){ return item.id.replace(item_delimiter, '') }).join(item_delimiter),
                    product_name: items.map(function(item){ return item.name.replace(item_delimiter, '').replace(/\s{2,}/g,' ') }).join(item_delimiter),
                    delimiter: item_delimiter,
                }
            } },
        // product detail
        {   px: mediamath_pixel.item_detail, 
            v: try_pagetrack(/product detail$/i),  
            a: function() { 
                
                
                var item_price = element_text('#price-list04 [class^="BT_price"]');
                var item_discount = element_text('#price-list06 [class^="BT_price"]') || element_text('#price-list05 [class^="BT_price"]');
                var ratings = element_text('#ttalk_rating_div > div > div[id] > span:nth-child(2) > strong:first-child');

                var item_info = {
                    product_id: digitalData.product.model_code,
                    product_name: digitalData.product.displayName,
                    product_category: digitalData.product.category,
                    product_category_id: element_attr('input#categoryTypeCode', 'value'),
                    currency: 'KRW',
                    // product_rating: text_to_int()
                    product_status: /판매중/.test(element_attr('input#instock', 'value')) ? 'in stock' : 'out of stock',
                }

                if(item_price)
                    item_info.product_price = text_to_int(item_price);
                if(item_discount)
                    item_info.product_discount_price = text_to_int(item_discount);
                if(ratings)
                    item_info.product_rating = text_to_int(ratings)/1.0e1;


                var btn_selectors = {
                    '#BT_btn-cart': mediamath_pixel.add_cart, 
                    '#BT_btn-buy': mediamath_pixel.add_cart,
                    '.store-reservation > a': mediamath_pixel.add_wish
                };
                // set button clicks
                Object.keys(btn_selectors).forEach(function(selector) {
                    var bts = document.querySelectorAll(selector);
                    if(bts && 0<bts.length) {
                        bts.forEach(function(bt) {
                            bt.addEventListener('click', function() {
                                mm_pixel(btn_selectors[selector], item_info);
                            });
                        });
                    }
                });
                return item_info;
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