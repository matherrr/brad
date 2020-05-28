(function() {
    // google ads
    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };
    
    // Google pageview (공통)
    if(!window.dataLayer) {
        window.dataLayer = [];
    }

    if(!window.gtag) {
        window.gtag = function() { window.dataLayer.push(arguments); }
        gtag('js', new Date());
    }

    // const gaid = '';   GA id 필요 
    const gcid = 'AW-805732128';
    
    // GDN
    _create_element('script', {
        async: true,
        src: 'https://www.googletagmanager.com/gtag/js?id='+gcid,
    }, document.head, null , 'script[src*="https://www.googletagmanager.com/gtag"]');
    
    gtag('config', gcid); 


    ga_key = {
        'button.my-edition_btn.save_btn': '86Z-CKzxzMwBEKD-mYAD',  // 저장하기 클릭
        'button.my-edition_btn.buy_btn': 'Bf7tCJnzzMwBEKD-mYAD',  // 구매하기 클릭
    }



    // google ads
    Object.keys(ga_key).forEach(function(selector) {
        let ga_code = ga_key[selector];
        document.querySelectorAll(selector).forEach(function(btn) {
            btn.addEventListener('click', function() {
                
                window.gtag('event','conversion',{'send_to': 'AW-805732128/'+ga_code, 'event_callback':callback});

            });
        });
    }); 
    
})();
