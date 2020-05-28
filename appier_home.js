/* www.samsung.com/sec/ 이 페이지 에서만.
 - Add to wishlist, Add to Shopping cart 제외 모든 pageview 기반 스크립트 사용
*/
(function() {
    // appier 스크립트를 로드한다.
    window.appier_q = window.appier_q || [];

    window.appier_q.push(
        {"t": "register", "content": { "id": "1MAA", "site": "samsung.com" }},
        {"t": "type_home","content": ""}
    );
})();