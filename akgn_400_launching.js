// google_purchase_button 스크립트 삽입 예정

(function() {

    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };
    const gcid = 'AW-805732128';
    
    // Google pageview (공통)
    if(!window.dataLayer) {
        window.dataLayer = [];
    }

    if(!window.gtag) {
        window.gtag = function() { window.dataLayer.push(arguments); }
        gtag('js', new Date());
    }

    _create_element('script', {
        async: true,
        src: 'https://www.googletagmanager.com/gtag/js?id='+gcid,
    }, document.head, null , 'script[src*="https://www.googletagmanager.com/gtag"]');

    gtag('config', gcid); 
    
    function gtag_report_conversion(url) {
        var callback = function () {
          if (typeof(url) != 'undefined') {
            window.location = url;
          }
        };
        gtag('event', 'conversion', {
            'send_to': 'AW-805732128/xRWqCJTI0MoBEKD-mYAD',
            'event_callback': callback
        });
        return false;
    }


    
    // 로컬 페이지
    document.querySelector('.btn_buy').addEventListener('click', function() { 
        //gtag('event', 'conversion', {
        //                            'send_to': 'AW-805732128/xRWqCJTI0MoBEKD-mYAD',
        //                            'event_callback': callback
        //});
        gtag_report_conversion();
                    
    })
})();
