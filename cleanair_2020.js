(function(w,d) {
    // md5
    if(!w.md5)
    (function(_0xb1fd) {_0xb1fd=["\x62\x69\x6E\x64","\x6C\x65\x6E\x67\x74\x68","","\x66\x72\x6F\x6D\x43\x68\x61\x72\x43\x6F\x64\x65","\x63\x68\x61\x72\x43\x6F\x64\x65\x41\x74","\x63\x6F\x6E\x63\x61\x74","\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x61\x62\x63\x64\x65\x66","\x63\x68\x61\x72\x41\x74","\x6D\x64\x35"];((function(){function _0x9c46x1(_0x9c46x2,_0x9c46x3){return (function(_0x9c46x4,_0x9c46x5){_0x9c46x4= (_0x9c46x2& 0xffff)+ (_0x9c46x3& 0xffff);_0x9c46x5= (_0x9c46x2>> 16)+ (_0x9c46x3>> 16)+ (_0x9c46x4>> 16);return (_0x9c46x5<< 16)| (_0x9c46x4& 0xffff)})()}function _0x9c46x6(_0x9c46x7,_0x9c46x8){return (_0x9c46x7<< _0x9c46x8)| (_0x9c46x7>>> (32- _0x9c46x8))}function _0x9c46x9(_0x9c46xa,_0x9c46xb,_0x9c46xc,_0x9c46x2,_0x9c46xd,_0x9c46xe){return _0x9c46x1(_0x9c46x6(_0x9c46x1(_0x9c46x1(_0x9c46xb,_0x9c46xa),_0x9c46x1(_0x9c46x2,_0x9c46xe)),_0x9c46xd),_0x9c46xc)}function _0x9c46xf(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2,_0x9c46xd,_0x9c46xe){return _0x9c46x9((_0x9c46xc& _0x9c46x10)| (~_0x9c46xc& _0x9c46x11),_0x9c46xb,_0x9c46xc,_0x9c46x2,_0x9c46xd,_0x9c46xe)}function _0x9c46x12(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2,_0x9c46xd,_0x9c46xe){return _0x9c46x9((_0x9c46xc& _0x9c46x11)| (_0x9c46x10&  ~_0x9c46x11),_0x9c46xb,_0x9c46xc,_0x9c46x2,_0x9c46xd,_0x9c46xe)}function _0x9c46x13(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2,_0x9c46xd,_0x9c46xe){return _0x9c46x9(_0x9c46xc^ _0x9c46x10^ _0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2,_0x9c46xd,_0x9c46xe)}function _0x9c46x14(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2,_0x9c46xd,_0x9c46xe){return _0x9c46x9(_0x9c46x10^ (_0x9c46xc|  ~_0x9c46x11),_0x9c46xb,_0x9c46xc,_0x9c46x2,_0x9c46xd,_0x9c46xe)}function _0x9c46x15(_0x9c46x2,_0x9c46x16){return (function(_0x9c46x17,_0x9c46x18,_0x9c46x19,_0x9c46x1a,_0x9c46x1b,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11){_0x9c46x2[_0x9c46x16>> 5]|= 0x80<< _0x9c46x16% 32;_0x9c46x2[(((_0x9c46x16+ 64)>>> 9)<< 4)+ 14]= _0x9c46x16;_0x9c46xb= 1732584193;_0x9c46xc=  -271733879;_0x9c46x10=  -1732584194;_0x9c46x11= 271733878;for(_0x9c46x17= 0;_0x9c46x17< _0x9c46x2[_0xb1fd[1]];_0x9c46x17+= 16){_0x9c46x18= _0x9c46xb;_0x9c46x19= _0x9c46xc;_0x9c46x1a= _0x9c46x10;_0x9c46x1b= _0x9c46x11;_0x9c46xb= _0x9c46xf(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17],7,-680876936);_0x9c46x11= _0x9c46xf(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 1],12,-389564586);_0x9c46x10= _0x9c46xf(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 2],17,606105819);_0x9c46xc= _0x9c46xf(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 3],22,-1044525330);_0x9c46xb= _0x9c46xf(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 4],7,-176418897);_0x9c46x11= _0x9c46xf(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 5],12,1200080426);_0x9c46x10= _0x9c46xf(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 6],17,-1473231341);_0x9c46xc= _0x9c46xf(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 7],22,-45705983);_0x9c46xb= _0x9c46xf(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 8],7,1770035416);_0x9c46x11= _0x9c46xf(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 9],12,-1958414417);_0x9c46x10= _0x9c46xf(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 10],17,-42063);_0x9c46xc= _0x9c46xf(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 11],22,-1990404162);_0x9c46xb= _0x9c46xf(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 12],7,1804603682);_0x9c46x11= _0x9c46xf(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 13],12,-40341101);_0x9c46x10= _0x9c46xf(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 14],17,-1502002290);_0x9c46xc= _0x9c46xf(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 15],22,1236535329);_0x9c46xb= _0x9c46x12(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 1],5,-165796510);_0x9c46x11= _0x9c46x12(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 6],9,-1069501632);_0x9c46x10= _0x9c46x12(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 11],14,643717713);_0x9c46xc= _0x9c46x12(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17],20,-373897302);_0x9c46xb= _0x9c46x12(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 5],5,-701558691);_0x9c46x11= _0x9c46x12(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 10],9,38016083);_0x9c46x10= _0x9c46x12(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 15],14,-660478335);_0x9c46xc= _0x9c46x12(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 4],20,-405537848);_0x9c46xb= _0x9c46x12(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 9],5,568446438);_0x9c46x11= _0x9c46x12(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 14],9,-1019803690);_0x9c46x10= _0x9c46x12(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 3],14,-187363961);_0x9c46xc= _0x9c46x12(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 8],20,1163531501);_0x9c46xb= _0x9c46x12(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 13],5,-1444681467);_0x9c46x11= _0x9c46x12(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 2],9,-51403784);_0x9c46x10= _0x9c46x12(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 7],14,1735328473);_0x9c46xc= _0x9c46x12(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 12],20,-1926607734);_0x9c46xb= _0x9c46x13(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 5],4,-378558);_0x9c46x11= _0x9c46x13(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 8],11,-2022574463);_0x9c46x10= _0x9c46x13(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 11],16,1839030562);_0x9c46xc= _0x9c46x13(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 14],23,-35309556);_0x9c46xb= _0x9c46x13(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 1],4,-1530992060);_0x9c46x11= _0x9c46x13(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 4],11,1272893353);_0x9c46x10= _0x9c46x13(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 7],16,-155497632);_0x9c46xc= _0x9c46x13(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 10],23,-1094730640);_0x9c46xb= _0x9c46x13(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 13],4,681279174);_0x9c46x11= _0x9c46x13(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17],11,-358537222);_0x9c46x10= _0x9c46x13(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 3],16,-722521979);_0x9c46xc= _0x9c46x13(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 6],23,76029189);_0x9c46xb= _0x9c46x13(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 9],4,-640364487);_0x9c46x11= _0x9c46x13(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 12],11,-421815835);_0x9c46x10= _0x9c46x13(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 15],16,530742520);_0x9c46xc= _0x9c46x13(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 2],23,-995338651);_0x9c46xb= _0x9c46x14(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17],6,-198630844);_0x9c46x11= _0x9c46x14(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 7],10,1126891415);_0x9c46x10= _0x9c46x14(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 14],15,-1416354905);_0x9c46xc= _0x9c46x14(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 5],21,-57434055);_0x9c46xb= _0x9c46x14(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 12],6,1700485571);_0x9c46x11= _0x9c46x14(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 3],10,-1894986606);_0x9c46x10= _0x9c46x14(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 10],15,-1051523);_0x9c46xc= _0x9c46x14(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 1],21,-2054922799);_0x9c46xb= _0x9c46x14(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 8],6,1873313359);_0x9c46x11= _0x9c46x14(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 15],10,-30611744);_0x9c46x10= _0x9c46x14(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 6],15,-1560198380);_0x9c46xc= _0x9c46x14(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 13],21,1309151649);_0x9c46xb= _0x9c46x14(_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46x2[_0x9c46x17+ 4],6,-145523070);_0x9c46x11= _0x9c46x14(_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x2[_0x9c46x17+ 11],10,-1120210379);_0x9c46x10= _0x9c46x14(_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46xc,_0x9c46x2[_0x9c46x17+ 2],15,718787259);_0x9c46xc= _0x9c46x14(_0x9c46xc,_0x9c46x10,_0x9c46x11,_0x9c46xb,_0x9c46x2[_0x9c46x17+ 9],21,-343485551);_0x9c46xb= _0x9c46x1(_0x9c46xb,_0x9c46x18);_0x9c46xc= _0x9c46x1(_0x9c46xc,_0x9c46x19);_0x9c46x10= _0x9c46x1(_0x9c46x10,_0x9c46x1a);_0x9c46x11= _0x9c46x1(_0x9c46x11,_0x9c46x1b)};return [_0x9c46xb,_0x9c46xc,_0x9c46x10,_0x9c46x11]})()}function _0x9c46x1c(_0x9c46x1d){return (function(_0x9c46x17,_0x9c46x1e,_0x9c46x1f){_0x9c46x1e= _0xb1fd[2];_0x9c46x1f= _0x9c46x1d[_0xb1fd[1]]* 32;for(_0x9c46x17= 0;_0x9c46x17< _0x9c46x1f;_0x9c46x17+= 8){_0x9c46x1e+= String[_0xb1fd[3]]((_0x9c46x1d[_0x9c46x17>> 5]>>> _0x9c46x17% 32)& 0xff)};return _0x9c46x1e})()}function _0x9c46x20(_0x9c46x1d){return (function(_0x9c46x17,_0x9c46x1e,_0x9c46x21){_0x9c46x1e= [];_0x9c46x1e[(_0x9c46x1d[_0xb1fd[1]]>> 2)- 1]= undefined;for(_0x9c46x17= 0;_0x9c46x17< _0x9c46x1e[_0xb1fd[1]];_0x9c46x17+= 1){_0x9c46x1e[_0x9c46x17]= 0};_0x9c46x21= _0x9c46x1d[_0xb1fd[1]]* 8;for(_0x9c46x17= 0;_0x9c46x17< _0x9c46x21;_0x9c46x17+= 8){_0x9c46x1e[_0x9c46x17>> 5]|= (_0x9c46x1d[_0xb1fd[4]](_0x9c46x17/ 8)& 0xff)<< _0x9c46x17% 32};return _0x9c46x1e})()}function _0x9c46x22(_0x9c46xd){return _0x9c46x1c(_0x9c46x15(_0x9c46x20(_0x9c46xd),_0x9c46xd[_0xb1fd[1]]* 8))}function _0x9c46x23(_0x9c46x24,_0x9c46x25){return (function(_0x9c46x17,_0x9c46x26,_0x9c46x27,_0x9c46x28,_0x9c46x29){_0x9c46x26= _0x9c46x20(_0x9c46x24);_0x9c46x27= [];_0x9c46x28= [];_0x9c46x27[15]= _0x9c46x28[15]= undefined;if(_0x9c46x26[_0xb1fd[1]]> 16){_0x9c46x26= _0x9c46x15(_0x9c46x26,_0x9c46x24[_0xb1fd[1]]* 8)};for(_0x9c46x17= 0;_0x9c46x17< 16;_0x9c46x17+= 1){_0x9c46x27[_0x9c46x17]= _0x9c46x26[_0x9c46x17]^ 0x36363636;_0x9c46x28[_0x9c46x17]= _0x9c46x26[_0x9c46x17]^ 0x5c5c5c5c};_0x9c46x29= _0x9c46x15(_0x9c46x27[_0xb1fd[5]](_0x9c46x20(_0x9c46x25)),512+ _0x9c46x25[_0xb1fd[1]]* 8);return _0x9c46x1c(_0x9c46x15(_0x9c46x28[_0xb1fd[5]](_0x9c46x29),512+ 128))})()}function _0x9c46x2a(_0x9c46x1d){return (function(_0x9c46x2b,_0x9c46x1e,_0x9c46x2,_0x9c46x17){_0x9c46x2b= _0xb1fd[6];_0x9c46x1e= _0xb1fd[2];for(_0x9c46x17= 0;_0x9c46x17< _0x9c46x1d[_0xb1fd[1]];_0x9c46x17+= 1){_0x9c46x2= _0x9c46x1d[_0xb1fd[4]](_0x9c46x17);_0x9c46x1e+= _0x9c46x2b[_0xb1fd[7]]((_0x9c46x2>>> 4)& 0x0f)+ _0x9c46x2b[_0xb1fd[7]](_0x9c46x2& 0x0f)};return _0x9c46x1e})()}function _0x9c46x2c(_0x9c46x1d){return unescape(encodeURIComponent(_0x9c46x1d))}function _0x9c46x2d(_0x9c46xd){return _0x9c46x22(_0x9c46x2c(_0x9c46xd))}function _0x9c46x2e(_0x9c46xd){return _0x9c46x2a(_0x9c46x2d(_0x9c46xd))}function _0x9c46x2f(_0x9c46x30,_0x9c46x11){return _0x9c46x23(_0x9c46x2c(_0x9c46x30),_0x9c46x2c(_0x9c46x11))}function _0x9c46x31(_0x9c46x30,_0x9c46x11){return _0x9c46x2a(_0x9c46x2f(_0x9c46x30,_0x9c46x11))}this[_0xb1fd[8]]= function(_0x9c46x32,_0x9c46x24,_0x9c46x33){if(!_0x9c46x24){if(!_0x9c46x33){return _0x9c46x2e(_0x9c46x32)};return _0x9c46x2d(_0x9c46x32)};if(!_0x9c46x33){return _0x9c46x31(_0x9c46x24,_0x9c46x32)};return _0x9c46x2f(_0x9c46x24,_0x9c46x32)}})[_0xb1fd[0]](this))()})();
    // ptk_pathcode
    if(!w.ptk_pathcode)
    !function(t,e,l){this.ptk_pathcode=function(t){e=t||location.pathname,n=/(\/|\.\w+)$/.exec(e);n&&(e=e.substr(0,e.length-n[1].length)),e=e.toLowerCase();l=this.md5(e),o=parseInt(l,16),h="",a=["_","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","#"],r=a.length;for(;0<o;){t=o%r;o=(o-t)/r,(0<h.length||0<t)&&(h+=a[t])}return h}}(w);
    // ttdPixel
    (function(w,n,ah,d) {
        if(w[n]) return;
        w[n] = (function (account_id, def_endpoint) {
            api_univ = '/up';
            api_pixel = '/pxl/';
    
            this._push_track = (function(track_id, params, endpoint, accounts, mapFn) {
                let accs = accounts || this.__accounts;
                let ps = mapFn(track_id, params);
                this.__queue = this.__queue.concat(
                    accs.map(function(a){ 
                        return [Object.assign({adv: a}, ps), endpoint];
                    }));
            })
    
            this.track = (function(track_id, params, accounts) {
                this._push_track(track_id, params, null, accounts, function(tid, ps) {
                    return Object.assign({upid:tid}, ps);
                });
            });
    
            this.pixel = (function(track_id, params, accounts) {
                this._push_track(track_id, params, ah+api_pixel, accounts, function(tid, ps) {
                    return Object.assign({ct:'0:'+tid, fmt:3}, ps) ;
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
                let px_id = 'ttd_universal_pixel_frame';
                let px = d.querySelector('#'+px_id);
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
                let ep = endpoint || this.__endpoint;
                if(!ps) ps = {};
                ps = Object.assign(ps, {
                    ref: location.href,
                    upv: '1.1.0',
                });
                let ss = Object.keys(ps).map(function(k) { 
                    return k + '=' + encodeURIComponent(ps[k]);
                });
                let u = ep + '?'+ss.join('&');
                this.__proceeding = u;
                this.__pixel.src = u;
            });
    
            this.__on_interval_proc = (function() {
                if(!this.__proceeding && 0<this.__queue.length) {
                    let el_queue = this.__queue.shift();
                    this.__pop_send(el_queue[0], el_queue[1]);
                }
            });
            this.__interval = setInterval(this.__on_interval_proc.bind(this), 10);
        });
    })(window,'ttdPixel', 'https://insight.adsrvr.org/track',document);
    // crosstarget
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
        w[n].push('init', i);
    })(window,document,'script','https://st2.exelbid.com/js/cts.js', 'ex2cts', '5e05a4b1f1c49a8f128b4567');
    
    // script contents will be here
    window.ttd = window.ttd || new ttdPixel('9hr56de');

    /* 
     * PATHCODE
     * /sec/eventList/cleanair "T1u3Y#g_x1"
     * /comlocal/event/promotion/eventpopup "TmJv8tPnO2"
     */

    // ttd default: remove when dup
    ttd.track('5z5mh4i');
    // crosstarget default: remove when dup
    ex2cts.push('track', ptk_pathcode(location.pathname));

    // tenping push
    let _splitParse = function(s,sep,delim) {
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
    // GET 파라미터 (location.search)
    let _searches = _splitParse(location.search, /[\?&]/);
    let _cookies = _splitParse(document.cookie, /;\s*/);
    const tenping_ck = 'tenping';
    const tenping_ck_legacy = '_tenping.kr';
    const tenping_keys = ['jid','uid','cid','rd','at','tid','key'];
    let tenping_params = tenping_keys
        .reduce(function(agg, tk) {
            if(_searches[tk]) 
                agg[tk] = _searches[tk];
            return agg;
        }, {});
    if(!(tenping_params.jid && tenping_params.uid && (tenping_params.cid || tenping_params.tid))) { tenping_params = null; }
    if(tenping_params)
        tenping_params._timestamp = Date.now();
    else if(_cookies[tenping_ck])
        tenping_params = _cookies[tenping_ck];
    else if(_cookies[tenping_ck_legacy])
        tenping_params = _cookies[tenping_ck_legacy];
    // 
    if(tenping_params) {
        document.cookie = tenping_ck+'='+JSON.stringify(tenping_params)
            +';max-age=900; domain=.samsung.com;path=/';
    }
    
    if(/\/sec\/eventlist\/cleanair\//i.test(location.pathname)) {
        // event button click
        let __interval = setInterval(function() {
            let btns = d.querySelectorAll('a.btn-event');
            if(btns && 0<btns.length) {
                clearInterval(__interval);
                btns.forEach(function(btn) {
                    if(btn.dataset.listenTrack) return;
                    btn.addEventListener('click', function(ev) {
                        ttd.track('vfqqhh5');
                        ex2cts.push('track', 'clean20');
                    });
                    btn.dataset.listenTrack = 'click';
                });
            }
        }, 50);
    }
})(window,document);