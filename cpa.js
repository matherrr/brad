window.addEventListener('load', (function() {
    window.dataLayer = window.dataLayer || [];
    if(!gtag) {
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
    }

    const GID = 'UA-159340113-1';

    const search_keys = {
        tenping: ['jid','uid','rd','at', 'did', 'key'],
        tnk: ['adkey'],
    }

    const cookie_keys = {
        tenping: '_tenping.kr',
        tnk: '__twcc__',
    }

    // CID 해석
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
    let _cookies = split_parse(document.cookie, /;\s*/);
    let _searches = split_parse(location.search, /[\?&]/);

    // 
    const CID_KEYS = [
        'sitecode',
        'channel_category',
        'channel_type',
        'publisher',
        'product',
        'phase',
        'campaign', 
        'content_type',
        'creative',
        'segmentation',
    ];

    let utm_href = location.href;

    if(_searches.cid) {
        let tokens = _searches.cid.split(/_/);
        if(CID_KEYS.length <= tokens.length) {
            let campaigns = CID_KEYS.reduce((agg,ck,ci) => {
                agg[ck] = tokens[ci];
            });
            utm_searches = Object.assign({
                utm_campaign: campaigns.campaign.toLowerCase(),
                utm_source: campaigns.channel_type.toLowerCase(),
                utm_medium: campaigns.publisher.toLowerCase(),
                utm_content: campaigns.creative.toLowerCase(),
            }, _searches);

            // check if cpa values

            utm_href = location.protocol + '//' + location.hostname + location.pathname 
                + '?' + Object.keys(utm_searches)
                    .filter((uk)=>uk!='cid')
                    .map((uk) => uk+'='+ encodeURIComponent(utm_searches[uk]))
                    .join('&');
        }
    }

    gtag('config', GID, {
        user_id: '',
        page_location: utm_href

    });

}));