/* Local-B2C-AD-EVENT(RomanWedding_GA)-ALL */
(function(gaid, __importScript, sx, pn) {
    gaid = 'UA-100137701-4';
    let __importScript = function(url, onload) {
        sx = document.querySelector('script[src*="'+url+'"]');
        if(!sx) {
            sx = document.createElement('script');
            sx.async = true; sx.src = url; document.head.appendChild(sx);
            if(onload) sx.addEventListener('load', onload);    
        } else if(onload) {
            onload();        
        }
    }

    // gtag: google analytics
    __importScript('https://www.googletagmanager.com/gtag/js?id='+gaid, function() {
        window.gtag('js', new Date());
        window.gtag('config', gaid);
        window.gtag('config', 'AW-732374064');
    });
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){dataLayer.push(arguments);};

    document.querySelector('.btn_event > img').addEventListener('click', function(ev) {
        if(window.gtag) {
            pn = location.pathname.replace(/\/$/, '')+'/participate';
            gtag('config', 'UA-100137701-4', {page_path: pn});
            gtag('event', 'conversion', {'send_to': 'AW-732374064/19zKCMyt5q4BELDInN0C'})
        }
    });

    document.querySelector('.btn_event > img').addEventListener('click', function(ev) {
        if(window.gtag) {
            pn = location.pathname.replace(/\/$/, '')+'/participate';
            gtag('config', 'UA-100137701-4', {page_path: pn});
            gtag('event', 'conversion', {'send_to': ''})
        }
    });

    document.querySelectorAll('section.bottom_banner > a > img')
        .forEach(function(item) {
            item.addEventListener('click', function(ev) {
                if(window.gtag) {
                    pn = location.pathname.replace(/\/$/, '')+'/next';
                    gtag('config','UA-100137701-4', {page_path: pn});
                }
            });
        });
})();