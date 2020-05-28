/* 기본 appier script
 - Add to wishlist, Add to Shopping cart 제외 모든 pageview 기반 스크립트 사용
*/
(function() {
    // appier 스크립트를 로드한다.
    
    var path = location.pathname;
    var is_directory = function(pathname) {    
        return /^\/sec\/.+\/?(all-)?/.test(pathname) &&
        ['pfsearchDomain','pfcategoryLocalTitle','categoryTypeCode','categoryGroupCode'].reduce(function(gf,key) {
            return gf && !!document.querySelector('input[name="'+key+'"][value]');
        }, true);
    };
    //var dir_depth = document.querySelectorAll('li[property="itemListElement"');
    
    
    if (is_directory(path)) {
        window.appier_q = window.appier_q || [];
        var directory_items = function() {
            var item_ids = [];
            document.querySelectorAll('.product-grid .product-card').forEach(function(card) {
                var itemcode = card.getAttribute('data-omni');
                var codes = itemcode.split('|');
                if(codes && 1<codes.length)
                    itemcode = codes[1].trim();
                item_ids.push(itemcode);
            });
            return item_ids;
        };
        var dircode = document.querySelector('input[name="categoryTypeCode"]').value;
        var dirname = document.querySelector('input[name="pfcategoryLocalTitle"]').value;
        var appierRtCategory = [dircode,dirname]
        var appierRtProductIDList = directory_items();

        window.appier_q.push(
            {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
            {"t": "type_listpage","categoryIDs": appierRtCategory, "productIDList": appierRtProductIDList}
        );
    }
    
})();