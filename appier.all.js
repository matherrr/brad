/* 기본 appier script
 - Add to wishlist, Add to Shopping cart 제외 모든 pageview 기반 스크립트 사용
*/
(function() {
    // pd screen check
    // appier 스크립트를 로드한다.
    const appier_script_url = 'https://jscdn.appier.net/aa.js';
    var on_load_appier = function() {
        /* appier script 여기 */
        var path = location.pathname;
        window.appier_q.push(
            {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
            {"t":"pv_track","action_id": "c8e91b8001bf1cc","track_id":"zwCBPghxmhhwnQO","isCountReload": true,"counter": 0},
            {"t":"pv_track","action_id": "262cabae78a71cc","track_id":"zwCBPghxmhhwnQO","isCountReload": false,"counter": 1}
        );
    };
    
    if(document.querySelector('script[src*="'+appier_script_url+'"]')) {
        window.appier_q = window.appier_q || [];
        on_load_appier();
    } else {
        var script_element = document.createElement('script');
        script_element.async = true;
        script_element.src = appier_script_url + '?id=samsung.com';
        script_element.addEventListener('load', on_load_appier);
        document.head.appendChild(script_element);
    }
})();