
(function (_splitParse, _cookies, _induction_item_id, basket_items, params, params_str, induct_item,s2s) {

    _splitParse = function(s,sep,delim) {
        separator = sep || '&';
        delimiter = delim || '=';
        return s.split(separator).reduce(function(agg,t) {
            if(t && 0<t.length) {
                let ts = t.split(delimiter);
                let k = ts && 0<ts.length ? ts[0].toString() : null;
                let v = ts && 1<ts.length ? ts[1] : undefined;
                try { v = JSON.parse(v);} catch(ex) {}
                agg[k] = v;
            }
            return agg;
        },{});
    };

    _cookies = _splitParse(document.cookie, /;\s*/);
    _induction_item_id = /NZ60R(3|7)703P(W|K)B?/;
    basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));

    params = {
        advertiser_token : 213123123,
        click_key : _cookies.s2s_ck
    }
    params_str = Object.keys(params).map( (aa) => aa + '=' + params[aa]).join('&');

    if (basket_items){

        induct_item = basket_items.filter( function(i) {
            return i.id.match(_induction_item_id)
        })

        if (induct_item) {

            s2s = document.querySelector('script[src*="https://postback-ao.adison.co/api/postbacks/server"]');
            if (!s2s) {
                s2s = document.createElement('script');
                s2s.async = true;
                s2s.src = 'https://postback-ao.adison.co/api/postbacks/server?' + params_str;
                s2s.type = 'text/javascript';
                document.head.appendChild(s2s);
            }
        } 
    }
})();

