let items = [];
let hostpath = location.protocol + '//' + location.hostname;
document.querySelectorAll('li.cart-item').forEach(function(item) {
    try {
        let sku = item.querySelector('.cart-item-sku').textContent.trim();
        let qty = item.querySelector('input[name="quantity"]').value;
        qty = parseInt(qty);
        let price = item.querySelector('.item-price').textContent.replace(/[^\d]/g, '');
        let thumb = item.querySelector('.cart-item-thumb img[src]').src;
        let name = item.querySelector('.name').textContent.trim();

        if(!thumb.match(/^(\w+:)?\/\//))
            thumb = hostpath + thumb;
        let link = item.querySelector('a[href^="/sec/"]').href;
        if(!link.match(/^(\w+:)?\/\//))
            link = hostpath + link;
        price = parseInt(price)/qty;
        
        items.push({ 
            id: sku, 
            price: price, 
            quantity: qty,
            imgUrl: thumb, 
            name: name,
            category: '', 
            desc: '',
            link: link,
        });
    } catch(ex) { console.error(ex); }
});