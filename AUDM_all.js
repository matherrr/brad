(function(loc, _create_element,__AUDM){
    _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check, el) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };

    __AUDM = {
        '/sec/washing-machines/': '1410220',
        '/sec/vacuum-cleaners/': '1411544',
        '/sec/tvs/': '1410184',
        '/sec/refrigerators/': '1410211',
        '/sec/': '1390366',
        '/sec/kimchi-refrigerators/': '1459072',
        '/sec/electric-range/': '1410214',
        '/sec/eventList/cleanair/': '1458920',
        '/sec/dryers/': '1410221',
        '/sec/dishwashers/': '1459074',
        '/sec/cooking-appliances/': '1459073',
        '/sec/templateEvent/bespoke_weddingshop/': '1432787',
        '/sec/templateEvent/bespoke_buy/': '1424847',
        '/sec/bespoke/home/': '1424847',
        '/sec/airdresser/': '1390365',
        '/sec/air-conditioners/': '1410217',
        '/sec/air-cleaners/' : '1410230',
        '/sec/grande-ai/buy/': '1463354',
        '/sec/grande-ai/home/': '1463353',
    }
    if(!/\/$/.test(loc))
        loc = loc + '/';
    // console.log('audm matched', loc, __AUDM[loc]);
    if(__AUDM[loc]) {
        (function() {
            url = '//pixel.mathtag.com/event/js?mt_id='+__AUDM[loc]+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3='
            _create_element('script', {
                async: true,
                src: url,
            }, document.head, null, 'script[src*="'+url+'"]');
        })();
    }
})(location.pathname);

