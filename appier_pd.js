
/* PD 페이지*/
(function() {
    // 상품 코드
    var get_product_code = function() {
        var elem = document.querySelector('input#current_model_code[value]');
        return elem ? elem.value.trim() : null;
    }
    // 상품 가격
    var get_product_price = function() {
        var elem = document.querySelector('.product-details__info .BT_price:not([class*="del"])');
        if(!!elem) {
            try {
                return parseInt(elem.textContent.replace(/[^\d]+/g, ''));
            } catch (ex){
                return 0;
            }
        } else {
            return null;
        }
    }
    var product_code = get_product_code();
    var product_price = get_product_price();

    if(/\/sec\/.+\/.+\/?/.test(location.pathname) && !!product_code && product_price!=null) {
        window.appier_q = window.appier_q || [];

        var appierRtProduct = [{ 'productID': product_code, 'price': product_price }];
        window.appier_q.push(
            {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
            {"t": "type_product","itemList":appierRtProduct}
        );
    }
})();
