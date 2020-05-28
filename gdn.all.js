(function(url,mode_debug, __initiate, __condition, __resolved, resolve, __initiate, __interval) {
  // 초기화 함수
  let __initiate = function() {
    if(!window.gtag) {
      window.dataLayer = window.dataLayer || [];
      !function(f,b,e,v,n,t,s)
      {t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s)}(window, document,'script',
      'https://www.googletagmanager.com/gtag/js?id=AW-805732128');
      
      window.gtag = function() { dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', 'AW-805732128');
      gtag('config', 'AW-834540855');
    }
  }
  let __condition = function() {
    window.gtag;
  };
  let __resolved = function(rs) {
      /* TODO: 실행 코드 여기 */
      
  };
  let resolve = function(rs) {
      if(__interval) clearInterval(__interval);
      try {
          __resolved(rs);
      } catch(ex) { /* silence! */ }
  }

  __initiate();
  let __interval = setInterval(function(rs) {
      rs = __condition();
      return rs ? resolve(rs) : null;
  }, 5);
})(/* TODO: URL 여기 */);
  
