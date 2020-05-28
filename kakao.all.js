(function(url) {
    let __initiate = function() {
        if(!document.querySelector('script[src*="'+url+'"]')) {
            let se = document.createElement('script');
            se.async = true;
            se.src = url;
            se.type = 'text/javascript';
            se.async = true;
            document.head.appendChild(se);
        }
    }
    let __condition = function() {
        return window.kakaoPixel;
    };
    let __resolved = function(rs) {
        [
            '4991698368817838963',
            '2600209837813220190',
            '8632737926816088998',
            '736958750714606413',
        ].forEach(function(kpid) {
            kakaoPixel(kpid).pageView();
        });
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
    }, 5);  
})('https://t1.daumcdn.net/adfit/static/kp.js');