/* Local-B2C-AD-EVENT(Galaxy_Watch_KAKAKO)-All */
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


	}
  __condition = function() {
    return window.kakaoPixel;
  };
  __resolved = function(rs) {
    [
      '4991698368817838963',
      '736958750714606413',
    ].forEach(function(kpid){
      window.kakaoPixel(kpid).pageView('galaxy-watch');
      });
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