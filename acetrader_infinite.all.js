(function() {
    const client_id = '1867386465';
    const pixel_element_id = 'tracking_acetrader';
    const pixel_element_style = 'display:inline;position:absolute;right:0px;bottom:0px;width: 0px;height:0px;border:0px;padding:0px;margin:0px;background-color:transparent;';
    const pixel_attributes = {
        u: location.href,
        advid: client_id,
        r: document.referrer,
        code: document.characterSet,
        target: encodeURIComponent(JSON.stringify({oid: '', items: []})),
        action: 'custom1',
    }


    // 초기화 함수
    let __initiate = function() {
        if(!document.querySelector('#'+pixel_element_id)) {
            let pixel = document.createElement('img');
            pixel.id = pixel_element_id;
            pixel.style = pixel_element_style;
            pixel.src = 'https://adlc-exchange.toast.com/log?'
                + Object.keys(pixel_attributes).map(function(pk) {
                    return pk + '=' + encodeURIComponent(pixel_attributes[pk]);
                }).join('&');
            pixel.addEventListener('load', function() {
                pixel.loaded = 1;
            });
            document.body.appendChild(pixel);
        }
    }
    let __condition = function() {
        return document.querySelector('#'+pixel_element_id);
    };
    let __resolved = function(px) {
        console.log('AceTrader tracker', px, px.src);
        return;
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
    }, 1);
})();





/* tagType : custom1 으로 변경

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

    let _push_attr = function(){
        if(!window.ng_tgm_q){
            window.ng_tgm_q=[];
            window.ng_tgm_q.push({
                tagType:'custom1',
                device:'web',
                uniqValue:'',
                pageEncoding:'utf-8'
            });
        };
    };

    _create_element('script', {type:"text/javascript", src:"//static.tagmanager.toast.com/tag/view/1543" }, document.body, _push_attr ? {'load':_push_attr}: null)
})();

*/