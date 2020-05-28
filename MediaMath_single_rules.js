/* 
mt_id 가 룰마다 다 다름. 대략 16개 정도 
const로 id 리스트로 선언하고
forEach로 해결 단일룰로
mt_ids = []

추가해야할것. 각 제품페이지에서 해당픽셀 하나만 날라가야함
*/

/*
let id_path_set4 = {'/sec\/eventList\/galaxy_buds_plus/':'1410230',
                    '/sec\/eventList\/galaxy_buds_plus2/':'1410000'};
Object.keys(id_path_set4).forEach(function(path_key){ 
    if(path_key===location.pathname)   // --> 정규식으로??
    let mediamath_url = '//pixel.mathtag.com/event/js?mt_id='+id_path_set4[path_key]+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3=';
    _create_element('script', {
        async: true,
        src: mediamath_url,
    }, document.head, null, 'script[src*="//pixel.mathtag.com/event/js?mt_id='+id_path_set4[path_key]+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3="]')
    }); //id_path_set4[path_key]
*/

(function(){

    let mt_ids = ['1410230','1410217',.....];  // 추가하기
    let url_path = ['/sec\/event\/Jet_preorder/', .....]; // 추가하기
    let path_id_set = {'/sec\/event\/Jet_preorder/':'1410230'};  // 이렇게 가는걸루

    let _create_element = function(tag, attrs, appending_to, event_handlers, duplication_check) {
        if(duplication_check && document.querySelector(duplication_check)) return;

        let el = document.createElement(tag);
        Object.keys(attrs).forEach(function(ak) { el[ak] = attrs[ak]; });
        if(event_handlers)
            Object.keys(event_handlers).forEach(function(on){ el.addEventListener(on, event_handlers[on])});
        appending_to.appendChild(el);
        return el;
    };

    Object.keys(path_id_set).forEach(function(path){ 
        if(path===location.pathname){ // --> 정규식으로??
        var mediamath_url = '//pixel.mathtag.com/event/js?mt_id='+path_id_set[path]+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3=';
        _create_element('script', {
            async: true,
            src: mediamath_url,
        }, document.head, null, 'script[src*="//pixel.mathtag.com/event/js?mt_id='+path_id_set[path]+'&mt_adid=220452&mt_exem=&mt_excl=&v1=&v2=&v3=&s1=&s2=&s3="]');
      };
    });
    
})();

