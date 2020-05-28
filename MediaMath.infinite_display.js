
/* launch에서 let 구문 사용 가능? var 로 대체? */
/* mt=id = 1467799 로 변경 */

(function(){
    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };

    const mediamath_url = '//pixel.mathtag.com/event/js?mt_id=1467799&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3=';
    _create_element('script', {
        async: true,
        src: mediamath_url,
    }, document.head, null , 'script[src*="//pixel.mathtag.com/event/js?mt_id=1467799&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3="]');
})();



/* mathmedia 다른버전

(function(){
    let __loading = (function(d,u,x) {
        if(!d.querySelector('script[src*="'+u+'"]')) {
            let sc = d.createElement('script');
            sc.async=true; sc.src=u; 
            if(x)
                sc.addEventListener('load', x);
            d.head.appendChild(sc);
        } else if(x) {
            x();
        }
    });
    const mediamath_url = '//pixel.mathtag.com/event/js?mt_id=1467799&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3=';    
    
    __loading(window.document, mediamath_url);
    
})();
*/


