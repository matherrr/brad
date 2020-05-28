(function(url, _productDetailSection, se, __condition, __resolved, resolve, __initiate, __interval, rs) {
    _productDetailSection = document.querySelector('#product-detail');
    if(_productDetailSection) {
        // 초기화 함수
        __initiate = function() {
            if(!document.querySelector('script[src*="'+url+'"]')) {
                se = document.createElement('script');
                se.async = true;
                se.src = url;
                se.type = 'text/javascript';
                document.head.appendChild(se);
            }
        }
        __condition = function() {
            return window.criteo_q;
        };
        __resolved = function(rs) {
            try {
              (function(sitemode, sku_el, sku) {
                sitemode = 'd';
                if(window.width<=1024) sitemode = 'm';
                else if(window.width<=1440) sitemode = 't';
                sku_el = _productDetailSection.querySelector('.product-details__s-sku');
                sku = undefined;
                if(sku_el)
                    sku = sku_el.textContent.trim();
                else {
                    sku_el = _productDetailSection.querySelector('#currentModelName');
                    if(!sku_el) return;            
                    sku = sku_el.value;                  
                }
              	if(sku)
                  rs.push([
                      { event: "setAccount", account: 62197 },
                      { event: "setSiteType", type: sitemode },
                      { event: "viewItem", item: sku.trim() },
                  ]);
              })();
            } catch(ex) { /* console.error(ex); */ }
            
        };
        resolve = function() {
            if(__interval) clearInterval(__interval);
            try {    
                __resolved(rs);
            } catch(ex) { /* silence! */ }
        }

        __initiate();
        __interval = setInterval(function(rs) {
            rs = __condition();                  
            return rs ? resolve(rs) : null;
        }, 1);
    }                  
 })('https://static.criteo.net/js/ld/ld.js');                 
                  
                  
                  