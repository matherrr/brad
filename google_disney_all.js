(function(url) {
    var __initiate = function() {
        if(!document.querySelector('script[src*="'+url+'"]')) {
            var se = document.createElement('script');
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
    }
    var __condition = function() {
        return window.gtag;
    };
    var __resolved = function(gtag) {
        gtag('event', 'conversion', {'send_to': 'AW-805732128/hdF2CLjF780BEKD-mYAD'});
    }
    var resolve = function(rs) {
        if(__interval) clearInterval(__interval);
        try {
            __resolved(rs);
        } catch(ex) { /* silence! */ }
    }
  
    __initiate();
    var __interval = setInterval(function() {
        var rs = __condition();
        return rs ? resolve(rs) : null;
    }, 1);
  })('https://www.googletagmanager.com/gtag/js?id=AW-805732128');
  
  