(function(url,__initiate, __condition, __resolved, resolve, __initiate, __interval) {
  // 초기화 함수
  __initiate = function() {
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    
  }
  __condition = function() {
      return window.fbq;
  };
  __resolved = function(fbq, infocell, sku_el, sku, qty) {
    fbq('init', '211169836140452');
    fbq('init', '1040731766101815');
    infocell = document.querySelector('.product-details__info');
    sku_el = document.querySelector('.product-details__s-sku');
    sku = undefined;
    if(sku_el)
        sku = sku_el.textContent.trim();
    else {
        sku_el = document.querySelector('#currentModelName');
        if(!sku_el) return;
        sku = sku_el.value;
    }
    qty = 1;
    try {
      qty = parseInt(infocell.querySelector('.BT_amount input').value);
    } catch(ex) { }


    fbq('track', 'ViewContent', {
      content_type: 'product',
      content_ids: [sku],
      contents: [{
        id: sku,
        name: infocell.querySelector('[itemprop="name"]').textContent.trim(),
        quantity: qty,
      }],
      currency: 'KRW'
    });
  };
  resolve = function(rs) {
      if(__interval) clearInterval(__interval);
      try {
          __resolved(rs);
      } catch(ex) {}
  }

  __initiate();
  __interval = setInterval(function(rs) {
      rs = __condition();
      return rs ? resolve(rs) : null;
  }, 1);
})();