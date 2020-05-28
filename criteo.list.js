(function(url, __initiate, __condition, __resolved, resolve, __interval) {
      // 초기화 함수
      __initiate = function(se) {
          if(!document.querySelector('script[src*="'+url+'"]')) {
              se = document.createElement('script');
              se.async = true;
              se.src = url;
              se.type = 'text/javascript';
              se.async = true;
              document.head.appendChild(se);
          }
      }
      __condition = function() {
          return window.criteo_q;
      };
      __resolved = function(rs) {
        (function(sitemode, items, _products) {
          sitemode = 'd';
          if(window.width<=1024) sitemode = 'm';
          else if(window.width<=1440) sitemode = 't';
          items = [];
          _products = setInterval(function(cards) {
              cards = document.querySelectorAll('.product-card');
              if(cards && 0<cards.length) {
                  cards.forEach(function(card) {
                      try {
                        (function(sku_el, sku, matched) {
                          sku_el = card.querySelector('.product-card__prd-info-title-serial');
                          sku = sku_el ? sku_el.textContent : card.dataset.omni;
                          
                          sku = sku.trim();
                          matched = sku.match(/^(?<shortcode>[\w-_]+)\|(?<longcode>[\w-_]+)$/);
                          if(matched)
                              sku = matched.groups.longcode;
                          items.push(sku);
                        })();
                      } catch(ex) { }
                  });
                  rs.push([
                      { event: "setAccount", account: 62197 },
                      { event: "setSiteType", type: sitemode },
                      { event: "viewList", item: items },
                  ]);
                  clearInterval(_products);
              }
          }, 1);
        })();
      };
      resolve = function(rs) {
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
})('https://static.criteo.net/js/ld/ld.js');      
  