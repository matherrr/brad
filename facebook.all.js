(function() {
    let __initiate = function() {
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '211169836140452');
            fbq('init', '1040731766101815');
    }
    let __condition = function() {
        return window.fbq;
    };
    let __resolved = function(fbq) {
        fbq('track','PageView');
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
})();