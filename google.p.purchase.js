(function(url) {
  let __initiate = function() {
      if(!document.querySelector('script[src*="'+url+'"]')) {
          let se = document.createElement('script');
          se.async = true;
          se.src = url;
          se.type = 'text/javascript';
          se.async = true;
          document.head.appendChild(se);

          window.dataLayer = window.dataLayer || [];
          window.gtag = function() { dataLayer.push(arguments); }
          gtag('js', new Date());
        }
        gtag('config', 'AW-805732128');
        gtag('config', 'AW-834540855');
  }
  let __condition = function() {
      return window.gtag;
  };
  let __resolved = function(gtag) {
    let basket_items = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
    let order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);
    if(order_match && basket_items) {
      let order_id = order_match[1];
      let value = JSON.parse(window.sessionStorage.getItem('.checkout.revenue'));
      // sending...
      [
        'AW-805732128/2XvCCPT5toEBEKD-mYAD',
        'AW-834540855/dmmfCMGw3qUBELeq-I0D',
      ].forEach(function(target) {
        gtag('event', 'conversion', {
          send_to: target,
          value: value,
          currency: 'KRW',
          transaction_id: order_id,
        });
      });

      // 전환 태그. 한번에.
      [
        {
          filter: (item) => /^akgn400.{3}/i.test(item.id), 
          tag: 'AW-805732128/eB4aCLbItsoBEKD-mYAD', 
          value: (g,item) => { g+=parseInt(item.quantity); return g; }
        },
        {
          filter: (item)=> /^AR07T9170HCD/i.test(item.id),
          tag: 'AW-805732128/Yq9RCI7lhc0BEKD-mYAD',
          value: (g,item) => { return 1; },
        }
      ].forEach((conversion) => {
        let items = basket_items.filter(conversion.filter);
        if(items && 0<items.length) {
          gtag('event','conversion',{
            send_to: conversion.tag,
            value: items.reduce(conversion.value, 0),
            currency: conversion.currency || 'KRW',
            transaction_id: order_id
          })
        }
      });
    }
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
})('https://www.googletagmanager.com/gtag/js?id=AW-805732128');

