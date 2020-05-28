/* Legacy: Local-Shop-AN(KAKAO)-CM-Buy Action */
(function(url) {
    // 초기화 함수
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
    let __resolved = function(kp) {
        [
            '4991698368817838963',
            '2600209837813220190',
            '8632737926816088998',
            '736958750714606413',
        ].forEach(function(kpid) {
            window.kakaoPixel(kpid).viewCart();
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
    }, 1);    /* dtm코드기준 5->1로 변경 */
})('//t1.daumcdn.net/adfit/static/kp.js');