/* send :: /checkout/orderConfirmation/+ */
(function() {
    let _splitParse = function(s,sep,delim) {
        let separator = sep || '&';
        let delimiter = delim || '=';
        return s.split(separator).reduce(function(agg,t) {
            if(t && 0<t.length) {
                let ts = t.split(delimiter);
                let k = ts && 0<ts.length ? ts[0].toString() : null;
                let v = ts && 1<ts.length ? ts[1] : undefined;
                try { v = JSON.parse(v);} catch(ex) {}
                agg[k] = v;
            }
            return agg;
        }, {});
    };
    let _cookies = _splitParse(document.cookie, /;\s*/);
    const tenping_ck = '_tenping.kr';
    // 상품코드 from gosha 20191025. 
    // [NZ60R7703PWB, NZ60R3703PKB, NZ60R7703PW, NZ60R3703PK]
    // [DW60T7075FGECO, DW60T7075FSECO, DW50T4065FGECO, DW50T4065FSECO]


                
 
    // 20191025 카탈로그 목록 기준 중복 없음 확인.
    const tenping_item_id = /(NZ60R(3|7)703P(W|K)B?)|(DW(6|5)0T(7|4)0(7|6)5F(G|S)ECO)/;
                            
    // tenping 세션 로그 없으면 중단
    if(!_cookies[tenping_ck]) return;

    let tenping = function(params, onloadFn) {
        let img = document.createElement('img');
        img.id = tenping_ck;
        let params_str = Object.keys(params)
            .map((ok) => ok + '=' + params[ok])
            .join('&');
        img.src = 'http://api.tenping.kr/Query?' + params_str;
        img.onload = onloadFn;
        document.body.appendChild(img);
    }

    let order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);
    let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
    if(!basket_items) return;

    if(order_match && basket_items) {
        let order_id = order_match[1];
        let items = basket_items.filter(function(i) {
            return i.id.match(tenping_item_id);
        });
        if(!items || items.length<=0) return;
        
        let total_price = items.reduce(function(t,i) { 
            t += i.price * i.quantity;
            return t;
        }, 0);
        let total_qty = items.reduce(function(t,i) {
            t += i.quantity;
            return t;
        }, 0);
        if(0<total_price && 0<total_qty) {
            let params = Object.assign({
                ordnum: order_id,
                orddenum: 1,
                ordpri: total_price,
                itemnum: items.length,
                ordcom: Math.round(total_price*0.4),
                ordcnt: total_qty,
                taxType: 1370,
            }, _cookies[tenping_ck]);
            if(!document.querySelector('img#'+tenping_ck)) {
                tenping(params, function() {
                    document.cookie = tenping_ck+'=;domain=.samsung.com;path=/sec';
                });
            }
        }
    }
})();