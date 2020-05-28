/* appier 구매완료 스크립트
 - Add to wishlist, Add to Shopping cart 제외 모든 pageview 기반 스크립트 사용
*/
(function() {
    // appier 스크립트를 로드한다.
    window.appier_q = window.appier_q || [];
    
        
    var ItemList  = JSON.parse(window.sessionStorage.getItem('.checkout.items'));
    var order_match = /\/checkout\/orderConfirmation\/([\w-]+)/.exec(location.pathname);
    var appierRtorderId  = order_match[1];
    var appierRtPrice = JSON.parse(window.sessionStorage.getItem('.checkout.revenue'));
    var appierRtCurrency = 'KRW';
    var appierRtItemList = [];
    
    if (ItemList){
        ItemList.forEach(function(item) {
        
            if(item) {
                //item_info = JSON.parse(item_info);
    
                appierRtItemList.push({
                    productID: item.id,
                    unit: item.quantity,
                    price: Math.round(parseFloat(item.price)),
                });

            }
        });

        window.appier_q.push(
            { t: "register", "content": { "id": "1MAA", "site": "samsung.com" } },
            {"t":"type_purchase",  "itemList":appierRtItemList, 
                "totalvalue":appierRtPrice, 
                "currency":appierRtCurrency, 
                "action_id": "839384c4ed6b1cc",
                "track_id":"zwCBPghxmhhwnQO",
                "opts":{
                    "uu":appierRtorderId, 
                    "action_param1" : JSON.stringify(appierRtItemList), 
                    "action_param2": appierRtorderId,
                    "total_revenue" : appierRtPrice, 
                    "currency" : appierRtCurrency
                }
            }
        );
    }
})();