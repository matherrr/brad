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
        }
    }
    let __condition = function() {
        return window.gtag;
    };
    let __resolved = function(gtag) {
        gtag('js', new Date());
        gtag('config', 'AW-805732128');
        gtag('config', 'AW-834540855');
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


