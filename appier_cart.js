/* appier 구매완료 스크립트
 - Add to wishlist, Add to Shopping cart 제외 모든 pageview 기반 스크립트 사용
*/
(function() {
    // appier 스크립트를 로드한다.
    window.appier_q = window.appier_q || [];
    
    
    // var cart_quantity = document.querySelectorAll('input[name="quantity"]');
    var cart_items = document.querySelectorAll('li.cart-item');
    var revenue_total = 0;
    var items = [];

    cart_items.forEach(function(item) {
        var item_info = item.querySelector('form.cart-item-form').getAttribute('data-cart');
        if(item_info) {
            item_info = JSON.parse(item_info);

            items.push({
                productID: item.querySelectorAll('.cart-item-sku')[0].textContent,
                unit: item.querySelector('input[name="quantity"]').value,
                price: Math.round(parseFloat(item_info.productPostPrice)),
            });
            revenue_total += parseInt(item.querySelector('.item-price').textContent.replace(/[^\d]+/g, ''));
        }
    });

    // var cart_price = document.querySelectorAll('.cart-item-form');
    // var cart_name = document.querySelectorAll('.cart-item-sku');
    // var appierRtPrice = 0;
    // var appierRtCartList  = [];
    
    // for (var i = 0; i < cart_name.length; i++) {
    //     appierRtCartList.push({
    //         productID: cart_name[i].textContent,
    //         unit: cart_quantity[i].value,
    //         price: JSON.parse(cart_price[i].dataset.cart).productPostPrice
    //     })
    //     appierRtPrice +=cart_quantity[i].value*JSON.parse(cart_price[i].dataset.cart).productPostPrice;
    // }

    window.appier_q.push(
        {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
        {"t": "type_cart",  "itemList": items, "totalvalue" : revenue_total}
    );
          
    
})();