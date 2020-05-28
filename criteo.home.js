(function(url, __condition, __resolved, resolve, __initiate, __interval) {
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
    __resolved = function(cq, sitemode) {
        sitemode = 'd';
        if(window.width<=1024) sitemode = 'm';
        else if(window.width<=1440) sitemode = 't';

        criteo_q.push([
            { event: "setAccount", account: 62197 },
            { event: "setSiteType", type: sitemode },
            { event: "viewHome" },
        ]);
        
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
    }, 5);
})('https://static.criteo.net/js/ld/ld.js');