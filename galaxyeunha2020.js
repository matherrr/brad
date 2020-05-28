
(function(){
    if(!window.dataLayer) {
        window.dataLayer = [];
        function gtag(){dataLayer.push(arguments)} 
        gtag('js', new Date()); 
    }
    else if(!gtag) {
        function gtag(){dataLayer.push(arguments)} 
    }
    gtag('config', 'AW-725268762');

    if(/\/home/i.test(location.pathname)) {
        document.querySelectorAll('img.img-responsive.hand').forEach(function(btn){
            btn.addEventListener('click', function() {
                window.gtag('event','conversion',{'send_to': 'AW-725268762/BPl5CJH6g8kBEJry6tkC'});
            });
        });
    } else if(/\/apply/i.test(location.pathname)) {
        // do nothing
        // btn.setAttrubute('onclick', ''); 페이지 안넘어가게
    }

})();

