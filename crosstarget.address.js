(function(w,d,s,u,n,i,ss) {
    // prepare base
    w[n] = w[n] || {cmd: []};
    w[n].push = w[n].push || (function() { 
        if(w[n].callFunc)
            w[n].callFunc.apply(w[n], arguments);
        else 
            w[n].cmd.push(arguments);
    }).bind(w[n]);
    // create and injection
    if(!d.querySelector('script[src*="'+u+'"]')) {
        ss = d.createElement(s); ss.async = true; ss.src=u;
        d.head.appendChild(ss);
    }
    // push up
    w[n].push('init', i);

    // cart
    w[n].push('track', 'address');
})(window,document,'script','https://st2.exelbid.com/js/cts.js', 'ex2cts', '5e05a4b1f1c49a8f128b4567');
