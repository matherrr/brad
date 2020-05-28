(function(url, __initiate, __condition, __resolved, __interval, resolve) {
    // 초기화 함수
    __initiate = function(se) {
        if(!document.querySelector('script[src*="'+url+'"]')) {
            se = document.createElement('script');
            se.async = true;
            se.src = url;
            se.type = 'text/javascript';
            document.head.appendChild(se);
        }
        document.querySelector('.btn_event > img').addEventListener('click', function(ev) {
            if(window.kakaoPixel)
                window.kakaoPixel('3441035306879005618').purchase();
        });
    
        document.querySelectorAll('section.bottom_banner > a > img')
            .forEach(function(item) {
                item.addEventListener('click', function(ev) {
                    if(window.kakaoPixel)
                        window.kakaoPixel('7852098535930311871').purchase();
                });
            });
    }
    __condition = function() {
        return window.kakaoPixel;
    };
    __resolved = function(rs) {
        kakaoPixel('3441035306879005618').pageView();
        kakaoPixel('7852098535930311871').pageView();
        
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
})('https://t1.daumcdn.net/adfit/static/kp.js');