/* Local-B2C-AD-EVENT(RomanWedding_Facebook)-ALL */
// fbq: facebook
(function(fbid) {
    fbid = '1040731766101810';
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', fbid);
        fbq('track', 'PageView');

    // 이벤트 참여하기 버튼 클릭
    document.querySelector('.btn_event > img').addEventListener('click', function(ev) {
            if(window.fbq) {
                fbq('track', 'ViewContent', { content_name: 'romans_participate' });
            }
        });

    // 이벤트 자세히보기 버튼 클릭
    document.querySelectorAll('.section.bottom_banner > a > img')
        .forEach(function(item) {
            item.addEventListener('click', function(ev) {
                if(window.fbq) {
                    fbq('track', 'ViewContent', {content_name: 'romans_next'});
                }
            });
        });

})();