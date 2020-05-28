(function(url,mode_debug) {
    // 초기화 함수
    let __initiate = function() {
        if(!document.querySelector('script[src*="'+url+'"]')) {
            let se = document.createElement('script');
            se.async = true;
            se.src = url;
            se.type = 'text/javascript';
			se.async = true;
			document.head.appendChild(se);
		}
		window.ne_tgm_q = window.ne_tgm_q || [];
    }
    let __condition = function() {
		return window.ne_tgm_q;
    };
    let __resolved = function(ace) {
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
            } catch(ex) { console.log(ex); }
		});
		let puts = {
			tagType: 'cart',
			device: 'web',
			uniqValue: '',
			pageEncoding: document.characterSet,
			items: items,
		};
		console.log(puts);
        window.ne_tgm_q.push(puts);
    };
    let resolve = function(rs) {
        if(__interval) clearInterval(__interval);
        try {
            __resolved(rs);
        } catch(ex) { /* silence! */ }
    }

    __initiate();
    let __interval = setInterval(function() {
        let rs = __condition();
        return rs ? resolve(rs) : null;
    }, 1);
})('https://static.tagmanager.toast.com/tag/view/1543');