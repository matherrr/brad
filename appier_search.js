
/* PD 페이지*/
(function() {

    // appier 스크립트를 로드한다.
    // 상품 코드
    var path = location.pathname;
    var is_search = function(pathname) { return /^\/sec\/search\/?$/.test(pathname); }
    var search_keyword = function() {
        var mt = /searchvalue=([^&#]+)/i.exec(location.search);
        return mt ? decodeURIComponent(mt[1]) : null;
    };
    
    if (is_search(path) && search_keyword()){
        window.appier_q = window.appier_q || [];
        
        var appierRtProductIDList = [];
        var appierRtSearch = search_keyword();
        var search_item = document.querySelectorAll('ul[class*="result-list__items"] li[class*="list__item"] [class*="model-name"]');
        search_item.forEach( function(aa) {
            appierRtProductIDList.push(aa.textContent.trim().replace('모델명 : ',''));
        })
        window.appier_q.push(
            {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
            {"t": "type_listpage","keywords": appierRtSearch, "productIDList": appierRtProductIDList}
        );
    }
})();


