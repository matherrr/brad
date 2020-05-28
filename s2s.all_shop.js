/* cookie save */
(function(_splitParse, _searches, _cookies, s2s_ck, append_cookie) {
    // 문자열(s) 입력으로 받아 구분자 (sep, delim)에 따라 결과 오브젝트 {}로 반환하는 함수
    _splitParse = function(s,sep,delim, separator, delimiter) {
        separator = sep || '&';
        delimiter = delim || '=';
        return s.split(separator).reduce(function(agg,t) {
            if(t && 0<t.length) {
                (function(ts) {
                    ts = t.split(delimiter);
                    try {
                        k = ts[0] || '';
                        v = ts[1] || '';
                      agg[k] = v;
                    } catch(ex) { }
                })();
            }
            return agg;
        }, {});
    };

    // 최상단 함수 파라미터 마지막에 추가해야하나?
    append_cookie = function(key, value, options) {
        options = Object.assign(options || {}, common_cookie_option);
        document.cookie = key + '=' + value + '; ' + Object.keys(options).map((ok)=>ok +'='+ options[ok]).join('; ');
    };

    // GET 파라미터 (location.search)   *)처음 랜딩시에는 URL에 매체 파라미터를 가지고 있음
    _searches = _splitParse(location.search, /[\?&]/);
    // 쿠키 정보    *)다음 페이지 이동부터는 URL이 아닌 쿠키에 매체 파라미터 값을 가지고 있음
    _cookies = _splitParse(document.cookie, /;\s*/);

    // s2s.kr 용 상수 모음  , 가이드 확인시 click_key 파라미터만 쿠키에 물고 있으면 됨
    s2s_ck = '_s2s.kr';
    // 불필요 s2s_keys = ['click_key'];

    // 불필요 search_keys = Object.keys(_searches);
    // location.search 파라미터 중  s2s 서비스에 해당하는 값 모음

    if(!_searches.click_key){
        append_cookie(s2s_ck, _cookies.s2s_ck)
    }
    else{
        append_cookie(s2s_ck, _searches.click_key)
    }
}
)();





/*  추가 코드
    s2s_params = {
        advertiser_token : 111,
        click_key: _cookies.s2s_ck || _searches.click_key
    }

    s2s_params_str = Object.keys(s2s_params).map((pa) => pa + '=' + s2s_params[pa].join('&'));

    s2s_viewcontents = function(s2s_params_str) {
        s2s = document.querySelector('img[src*="https://postback-ao.adison.co/api/postbacks/server"]');
        if(!s2s) {
            s2s = document.createElement('img');
            s2s.async = true;
            s2s.src = 'https://postback-ao.adison.co/api/postbacks/server?'+ s2s_params_str;
            s2s.type ='text/javascript'
            document.head.appendChild(s2s);
        }
        };
    }
)();
*/