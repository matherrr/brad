(function() {
    // constants
    const GID = 'UA-159340113-1';
    const UTM_CAMPAIGN_DEFAULT = 'bespoke.2020';

    // gtag
    let utils = {
        html_element: function(tagname, attrs, appendTo, onLoad) {
            let se = document.createElement(tagname);
            Object.keys(attrs).forEach(function(ak) {
                se[ak] = attrs[ak];
            });
            se.addEventListener('load', onLoad);
            appendTo.appendChild(se);
        },
        };
    utils.import_script = function(u,o) {
        utils.html_element('script', {async: true, type: 'text/javascript', src: u}, document.head, o);
    };

    utils.import_script('https://www.googletagmanager.com/gtag/js');
    if(!window.dataLayer) {
        window.dataLayer = [];
    }
    if(!window.gtag) {
        window.gtag = function() { window.dataLayer.push(arguments); };
        gtag('js', new Date());
        }

    // utils
    let split_parse = function(s,sep,delim) {
        let separator = sep || '&';
        let delimiter = delim || '=';
        return s.split(separator).reduce(function(agg,t) {
            if(t && 0<t.length) {
                let ts = t.split(delimiter);
                let k = ts && 0<ts.length ? ts[0].toString() : null;
                let v = ts && 1<ts.length ? ts[1] : undefined;
                try { v = JSON.parse(v);} catch(ex) {}
                agg[k] = v;
            }
            return agg;
        }, {});
    };
    
    //
    let log_pageview = function() {
        if(!window.gtag) return;

        window.gtag('config', GID, {
            
            //page_path: path,     -> path 따로 지정해줄 필요 없음
            page_location: 'https://www.samsung.com/sec/templateEvent/bespoke_buy/?id=bespoke_color3' +   
                (utms ? '&' + Object.keys(utms).map((uk)=>'utm_'+uk+'='+utms[uk]).join('&') : ''),
        });
    }

    let __cookies = split_parse(document.cookie, /;\s*/);
    let __searches = split_parse(location.search, /[\?&]/);


    // CID to UTM
    let utms;
    let assign_utms = function(campaign, source, medium, content, term) {
        if(!utms) utms = {};

        // required
        utms.campaign = utms.campaign || campaign;
        utms.source = source;
        utms.medium = medium;

        // optional
        if(content) utms.content = content;
        if(term) utms.term = term;

        return utms;
    }
    
    // url에 utm 있을시
    if(__searches.utm_campaign) {
        utms = ['campaign','source','medium','content','term'].reduce(function(gg, uk) {
            if(__searches['utm_'+uk]) gg[uk] = __searches['utm_'+uk];
            return gg;
        }, {});
    } 
    // url에 cid 있을시
    else if(__searches.cid && typeof(__searches.cid)=='string') {
        let ctoks = __searches.cid.split('_');
        if(9<=ctoks.length) {
            assign_utms(ctoks[6] || UTM_CAMPAIGN_DEFAULT, ctoks[1], ctoks[3], ctoks[8], 10<=ctoks.length ? ctoks[9] : null);
        }
    }

    //실행단
    log_pageview();

})();