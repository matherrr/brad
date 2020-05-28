/* Local-Shop-AD(Criteo)-Checkout-All */
(function() {
    let ls = document.querySelector('ul.checkout-order-summary-list');
    let items = [];
    ls.querySelectorAll('li.checkout-order-summary-list-items').forEach((item) => {
        try {
            let qty = parseInt(item.querySelector('.details .product-classifications').textContent.replace(/[^\d]/g, ''));
            let cost = parseInt(item.querySelector('.product-price').textContent.replace(/[^\d]/g, ''));
            items.push({ 
                id: item.querySelector('.code').textContent.trim(),
                quantity: qty,
                price: Math.round(cost/qty),
            });
        } catch(ex) {
            console.error(ex);
        }
    });
    sessionStorage.setItem('.checkout.items', JSON.stringify(items));

    let value = items.reduce(function(t,item) {
        if(item.quantity && item.price)
            t += item.quantity * item.price;
        return t;
    }, 0);
    sessionStorage.setItem('.checkout.revenue', JSON.stringify(value));
})();