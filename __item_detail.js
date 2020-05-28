(function() {
    let sect = document.querySelector('#product-detail');
    return {
        id : sect.querySelector('input[id*="ModelName"]').value,
        name: sect.querySelector('[itemprop="name"]').textContent.replace(/(\s{2,}|[\r\n])/, ' ').trim(),
        quantity: parseInt(sect.querySelector('.BT_amount input').value),
    };
})();