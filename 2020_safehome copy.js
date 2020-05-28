//ttd pixel 심을 예정

(function(api_univ, api_pixel, accs, ps, px, px_id, ep, ss, u,  ttd_key) {
    // TTD

    (function(w,n,ah,d) {

        ttd_key = {
            '[data-scroll-btn=template01]': '4yio1hz',
            '[data-scroll-btn=template02]': '67crwa5',
            '[data-scroll-btn=template03]': 'pkuahdx',
            '[data-scroll-btn=template04]': 'q3icmso',
            '[data-scroll-btn=template05]': 'qrf7965',
            //'[ga-la*=IT]': 'vfqqhh5'
        }

        w[n] = w[n] || (function (account_id, def_endpoint) {
            api_univ = '/up';
            api_pixel = '/pxl/';
    
            this._push_track = (function(track_id, params, endpoint, accounts, mapFn) {
                accs = accounts || this.__accounts;
                ps = mapFn(track_id, params);
                this.__queue = this.__queue.concat(
                    accs.map(function(a){ 
                        return [Object.assign({adv: a}, ps), endpoint];
                    }));
            })
    
            this.track = (function(track_id, params, accounts) {
                this._push_track(track_id, params, null, accounts, function(tid) {
                    return {upid:tid};
                });
            });
    
            this.pixel = (function(track_id, params, accounts) {
                this._push_track(track_id, params, ah+api_pixel, accounts, function(tid) {
                    return {ct:'0:'+tid, fmt:3};
                });
            });
    
            this.__queue = [];
            this.__endpoint = def_endpoint || (ah + api_univ);
            this.__proceeding = null;
            
            this.__onload = (function() {
                this.__proceeding = null;
            });
            
            // constructor
            this.__accounts = [];
            this.__pixel = null;
            if(this.__accounts.indexOf(account_id.trim()) < 0) {
                this.__accounts.push(account_id);
            }
            if(!this.__pixel) {
                px_id = 'ttd_universal_pixel_frame';
                px = d.querySelector('#'+px_id);
                if(!px) {
                    px = d.createElement('iframe');
                    px.id = px_id;
                    px.width=0; px.height=0; px.style.display='none'; px.title='TTD Universal Pixel';
                    px.addEventListener('load', this.__onload.bind(this));
                    d.body.appendChild(px);
                }
                this.__pixel = px;
            }
    
            this.__pop_send = (function(ps, endpoint) {
                ep = endpoint || this.__endpoint;
                ps = Object.assign({
                    ref: location.href,
                    upv: '1.1.0',
                }, ps || {});
                ss = Object.keys(ps).map(function(k) { 
                    return k + '=' + encodeURIComponent(ps[k]);
                });
                u = ep + '?'+ss.join('&');
                this.__proceeding = u;
                this.__pixel.src = u;
            });
    
            this.__on_interval_proc = (function(el_queue) {
                if(!this.__proceeding && 0<this.__queue.length) {
                    el_queue = this.__queue.shift();
                    this.__pop_send(el_queue[0], el_queue[1]);
                }
            });
            this.__interval = setInterval(this.__on_interval_proc.bind(this), 10);
        }).bind(this);
    })(window,'ttdPixel', 'https://insight.adsrvr.org/track',document);
    
    Object.keys(ttd_key).forEach(function(selector) {
        let ttd_code = ttd_key[selector];
        document.querySelectorAll(selector).forEach(function(btn) {
            btn.addEventListener('click', function() {
                window.ttd = window.ttd || new ttdPixel('9hr56de');
                ttd.track(ttd_code);
            });
        });
    }); 
})();

