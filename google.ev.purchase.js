(function(productinfowrap, sku, priceline) {
  productinfowrap = document.querySelector('.product-details__info');
  sku = productinfowrap.querySelector('.product-details__info-top .product-details__s-sku').textContent;
  priceline = null;
  productinfowrap.querySelectorAll('.BT_price-sale').forEach(function(el){
    if(el.textContent && 0<el.textContent.trim().length)
      priceline = parseInt(el.textContent.replace(/[^\d]+/g, ''));
  });
  productinfowrap.querySelectorAll('.BT_price').forEach(function(el) {
    if(!priceline && el.textContent && 0<el.textContent.trim().length)
      priceline = parseInt(el.textContent.replace(/[^\d]+/g, ''));
  });
    
  gtag('event', 'conversion', {
    'send_to': 'AW-834540855/xyy-COTE3qUBELeq-I0D',
    'value': priceline,
    'currency': 'KRW',
    'transaction_id': sku
  });
})();
  