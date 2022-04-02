#! -*- coding: utf8 -*-

from dbproj.db_http import http
from dbproj.models import site
from dbproj import db_utils

import re
import time
import traceback
from datetime import datetime 
from urllib.parse import urlparse

__category_flat_pattern = re.compile(r'^(?P<pathname>[^\?#]+)')
#__category_all_pattern = re.compile(r'/all-[^/\?#]+')
__category_type_pattern = re.compile(r'/sec(/.+)*/(?P<title>[^/\?#]+)[/\?#]?')


def __validate_pathname(href) :
    path_match = __category_flat_pattern.match(href)
    if path_match is None : return None
    pathname = path_match['pathname']
    pathname += '/' if not pathname.endswith('/') else ''
    return pathname

def retrieve_categories_from(path, selector) :
    doc = http.get_sec_doc(path)
    links = http.query_select_all(doc, selector)
    cats = []
    # category candidate link urls
    for ln in links :
        href = ln['href']
        pathname = __validate_pathname(href)
        if pathname is None : continue
        cats.append(pathname)

    # requests to checkup
    categories = {}
    for idx,cat in enumerate(frozenset(cats)) :
        try :
            cdoc = http.get_sec_doc(cat)
            code_element = http.query_select(cdoc, '#categoryTypeCode')
            assert code_element is not None, 'category code element not found'
            ccode = code_element['value']
            assert ccode is not None and 0<int(ccode), 'invalid category type code'
            

            if ccode in categories and len(categories[ccode]) < len(cat) : 
                continue
            categories[ccode] = cat

            time.sleep(0)
        except :
            pass

    return categories

def __sec_image_url(suffix, *args, **kwargs) :
    rs = 'https://images.samsung.com/is/image/samsung/%s'%(suffix)
    if 0<len(args)+0<len(kwargs) :
        rs += '?'

    if 0<len(kwargs) :
        rs += '&'.join(['%s=%s'%p for p in kwargs.items()])
    if 0<len(args) :
        rs += ''.join(args)
    return rs


# 카테고리 목록 업데이트
# 
def check_categories(path='/sec/info/sitemap', selector='a[href*="/sec/"]') :
    # 현재 카테고리 목록 가져오기
    categories = retrieve_categories_from(path, selector)
    # 카테고리 목록 저장
    rss = site.discover_categories(categories)

def _visit_category_document(code, path) :
    doc = http.get_sec_doc(path)
    # update path to all- list
    if http.query_select(doc, '.filter-sort') is None :
        __pattern = r'/sec(?P<suffix>/.+)*/(?P<title>[^/\?#]+)[/\?#]?'
        __repl = '/sec\g<suffix>/\g<title>/all-\g<title>/'
        npath = re.sub(__pattern, __repl, path)
        
        if npath != path :
            doc = http.get_sec_doc(npath)
            path = npath

    # load filter data
    filters = http.sec_search_filters(code)


    
    return (doc, path, filters)

def __item_details_filter(fn, selector) :

    return [f for f in filter(lambda x: x is not None, mapping)]

__item_detail_src_pattern = re.compile(r'/(?P<path>sec-[^/\?\#]+/?)[\?\#]?.*$')
def __visit_category_items_detail_imageurls(element) :
    mt = __item_detail_src_pattern.search(element['src'])
    return mt.group('path') if mt is not None else None

__item_detail_desc_strip = re.compile(r'(\s{2,}|[\r\n])')
def __visit_category_items_detail_descriptions(section) :
    text = __item_detail_desc_strip.sub('', section.get_text())
    images = http.query_parse(section, 'img[src]', lambda img: img['src'])
    return (text,) + tuple(images)

def _visit_category_item_detail(model) :
    # skip priceless
    if __integer(model, 'price1Display') is None :
        return model
    doc = http.get_sec_doc(model['pdpUrl'])
    try : 
        model['largeImgs'] = http.query_parse(doc,
            '.product-details__view img[src]', 
            __visit_category_items_detail_imageurls)

        model['features'] = http.query_parse(doc,
            '#content section.feature-benefit',
            __visit_category_items_detail_descriptions)
        db_utils.timelog(' fetched model %s(%s) OK'%(model['displayName'], model['modelCode']))
    except :
        traceback.print_exc()
        db_utils.timelog(' error on fetching model %s(%s)!!'%(model['displayName'], model['modelCode']))
    
    return model

def _visit_category_items(cid,code) :
    # load item info
    item_data = {}
    items = site.discover_items(cid, code)
    visited_item_codes = []
    subcategories = {}
    puts = []
    dels = []

    for finfo in http.sec_search_items(code) :
        for model in finfo['modelList'] :
            try :
                mcode = model['modelCode']
                iid = items[mcode][0] if mcode in items else None
                visited_item_codes.append(mcode)
                try :
                    # update
                    scode = finfo['categorySubTypeCode'] if 'categorySubTypeCode' in finfo else code
                    if scode not in subcategories :
                        subcategories[scode] = finfo['fmyMarketingName']
                    
                    # down copy of model data
                    for fk in ('categoryFilId', 'chipOptions', 'categorySubTypeCode', 'fmyMarketingName'): 
                        try :
                            model[fk] = finfo[fk]
                        except:
                            continue
                    puts.append((iid,scode,mcode,_visit_category_item_detail(model)))
                except :
                    traceback.print_exc()
                    assert iid is not None 
                    dels.append((iid,traceback.format_exc()))
            except:
                pass

    try :
        item_data['subs'] = subcategories
        item_data['puts'] = [p for p in map(lambda put: put[0:3], puts)]
        item_data['dels'] = [d for d in map(lambda dx: dx, dels)]
    except:
        traceback.print_exc()
        pass

    for mcode,iinfo in items.items() :
        if mcode not in visited_item_codes :
            dels.append((iinfo[0], None))

    return (item_data, subcategories, puts, dels)


__breadcrumb_reduce_pattern = re.compile('([\r\n]+|\s{2,}|\/)')
def _visit_category_title(doc, code) :
    try:
        return http.query_select(doc, '#pfcategoryLocalTitle')['value']
    except:
        traceback.print_exc()
        return code

def _visit_category_breadcrumb(doc) :
    try :
        bcs = http.query_select_all(doc, '.cm-breadcrumb li')
        bc_tokens = map(lambda el: __breadcrumb_reduce_pattern.sub('', http.text_content(el)).strip(), bcs)
        return [str(t) for t in bc_tokens]
    except:
        traceback.print_exc()
        return []

def visit_category(cid,code,path) :
    # load filter info
    try :
        doc, path, filters = _visit_category_document(code, path)
        cdata, subs, puts, dels = _visit_category_items(cid, code)

        # category title
        title = code
        try:
            title = http.query_select(doc, '#pfcategoryLocalTitle')['value']
        except:
            traceback.print_exc()
            pass

        # Log
        db_utils.timelog('Category %s (%s) with %d items to puts, (%d) dels'%(
            title, code, len(puts), len(dels)
        ))
        title = _visit_category_title(doc, code)
        cdata['title'] = title
        cdata['breadcrumbs'] =  _visit_category_breadcrumb(doc)
        
        # push sub categories
        site.push_subcategories(cid, subs)
        # insert records
        for iid,scode,mcode,data in puts :
            if iid is not None :
                site.update_item(iid, scode, mcode, data, None)
            else :
                site.create_item(cid,scode,mcode,data)
        # delete non founds or errors
        for (iid,tbs) in dels :
            site.delete_item(iid, tbs)
        
        site.update_category(cid, title, path, cdata, filters)
    except:
        traceback.print_exc()
        site.error_category(cid, traceback.format_exc())

def _recent_items(limits=5, interval=1) :
    rss = site.recent_items(int(limits), int(interval))
    for rs in rss :
        print(rs)

def check_category_items(limits=4, interval=2) :
    # list recent categories
    categories = site.recent_categories(int(limits), int(interval))
    cids = [c for c in map(lambda cat: cat[0], categories)]
    site.mark_categories_visiting(cids)

    for cid,code,path in categories :
        visit_category(cid, code, path)

def __integer(mdata, key) :
    try :
        vstr = re.sub(r'[^\d]', '', mdata[key])
        return int(vstr)
    except :
        return None

def __number(mdata, key) :
    try :
        vstr = re.sub(r'[^\d\.]', '', mdata[key])
        return float(vstr)
    except :
        return None

def __str_contains(mdata, key, salt) :
    try :
        return salt in mdata[key]
    except :
        return False

def load_feed_data() :
    feed = {}
    category_ids = []
    subcategory_codes = []
    iteminfo = []

    for iid,cid,scode,mcode,mdata in site.list_items() :
        if cid not in category_ids :
            category_ids.append(cid)
        if scode not in subcategory_codes :
            subcategory_codes.append(scode)
        iteminfo.append({
            '_id': iid,
            'category_id': cid,
            'subcategory': scode,
            'model': mcode,
            'model_name': mdata['modelName'],
            'model_message': '\n'.join(mdata['marketingMessage']) if mdata['marketingMessage'] else '',
            'display_name': mdata['displayName'],
            'path': 'https://www.samsung.com%s'%(mdata['pdpUrl']),
            'thumbnail': __sec_image_url(mdata['thumbUrl']),
            'thumbnail_large': __sec_image_url(mdata['largeImgs'][0], '$PD_GALLERY_L_JPG$') if 'largeImgs' in mdata and 0<len(mdata['largeImgs']) else None,
            'images': [__sec_image_url(m) for m in mdata['galleryImage']],
            'price': __integer(mdata, 'price1Display'),
            'sales': __integer(mdata, 'price2Display'),
            'reviews': __integer(mdata, 'reviewCount'),
            'ratings': __number(mdata, 'ratings'),
            'points': __integer(mdata, 'samsungPoint'),
            'is_new': __str_contains(mdata, 'merchandisingText', '신상품'),
            'is_install': __str_contains(mdata, 'merchandisingText', '설치'),
            'is_pickable': __str_contains(mdata, 'merchandisingText', '픽업'),
            'is_discount': __str_contains(mdata, 'merchandisingText', '할인'),
            'is_limited': __str_contains(mdata, 'merchandisingText', '한정'),
            'is_soldout': __str_contains(mdata, 'merchandisingText', '품절'),
            'is_noncontract': __str_contains(mdata, 'merchandisingText', '무약정'),
            'is_details': __str_contains(mdata, 'ctaType', 'learnMore'),
        })
    
    # load categories
    categories = site.list_top_categories(category_ids)
    for cid,cat in categories.items() :
        # split category data
        ccode,cname,cdata = cat
        if 'breadcrumbs' in cdata :
            bcs = cdata['breadcrumbs']
            if bcs[-1] == '모든 모바일 액세서리' :
                bcs = bcs[0:-1] + ['모바일', '액세서리']
            elif bcs[-1].startswith('모든 ') and \
                (bcs[-1][3:] in bcs[-2] or bcs[-1] in bcs[-1]) :
                bcs = bcs[0:-1]
            cdata['breadcrumbs'] = ' > '.join(bcs)

    subcategories = site.list_sub_categories(subcategory_codes)
    for iid,iinfo in enumerate(iteminfo) :
        cid = iinfo['category_id']
        sc_code = iinfo['subcategory']
        if cid in categories :
            ccode, cname, cdata = categories[cid]
            iteminfo[iid]['category_code'] = ccode
            iteminfo[iid]['category_name'] = cname
            iteminfo[iid]['product_type'] = cdata['breadcrumbs'] if 'breadcrumbs' in cdata else None
        if sc_code in subcategories :
            pid, sc_code, sname = subcategories[sc_code]
            iteminfo[iid]['category_id'] = pid
            iteminfo[iid]['subcategory_name'] = sname
    
    return iteminfo

def __item_parse_name(d) :
    ms = re.split(r'\<br\s*\/?\>', d['display_name'], flags=re.I)
    return ms[0].strip() if ms is not None and 0<len(ms) else d['display_name']

def __item_parse_description(d):
    ms = re.split(r'\<br\s*\/?\>', d['display_name'], flags=re.I)
    content = '\n'.join(ms[1:]) if ms is not None and 1<len(ms) else d['model_message']
    content = re.sub(r'([\n\t]|\<br\s*\/?\>)', ' | ', d['model_message'])
    return content.strip()

def __build_item_parse_price(format:str) :
    def __item_parse_price(d) :
        if d['price'] is None :
            return '-'
        return format%(d['price'])
    return __item_parse_price

__item_parsemap_default = {
    'id': (lambda d: d['model'].strip()),
    'title': __item_parse_name,
    'description': __item_parse_description,
    'availability': (lambda d: 'out of stock' if d['is_soldout'] or d['price'] is None or d['price']<=0 else 'in stock'),
    'condition': (lambda d: 'new'),
    'price': __build_item_parse_price('%d'),
    'link': (lambda d: d['path'] if 'link' in d else ''),
    'image_link': (lambda d: d['thumbnail'] if 'thumbnail' in d else ''),
    'brand': (lambda d: d['subcategory_name'] if 'subcategory_name' in d else ''),
    'additional_image_link': (lambda d: d['images'][0] if d['images'] is not None and 0<len(d['images']) else ''),
    'item_group_id': (lambda d: d['subcategory']),
    'loyalty_points': (lambda d: '%d'%(d['points']) if d['points'] is not None else ''),
    'product_type': (lambda d: d['product_type'] if 'product_type' in d and d['product_type'] is not None else ''),
    'sale_price': (lambda d: '%d'%(d['sales']) if d['sales'] is not None and 0<d['sales'] else ''),
    'shipping': (lambda d: '0'),
    'mpn': (lambda d: d['model']),
    'custom_label_0': (lambda d: d['model_name'] if d['model_name'] is not None else ''),
    'custom_label_1': (lambda d: '설치' if d['is_install'] else ''),
    'custom_label_2': (lambda d: '픽업' if d['is_pickable'] else ''),
    'custom_label_3': (lambda d: '한정' if d['is_limited'] else ''),
    'custom_label_4': (lambda d: '상세' if d['is_details'] else ''),
}
__item_parsemap_additional_image = (lambda d: ','.join(d['images']) if d['images'] is not None and 0<len(d['images']) else '')
def __build_text_feed(fname, 
    columns:tuple, 
    parsemap=None, 
    prefix='',
    delimiter='\t') :
    iteminfo = load_feed_data()
    pmap = __item_parsemap_default.copy()
    if parsemap is not None :
        pmap.update(parsemap)
    with open('./output/%s'%(fname), 'w', encoding='utf8') as feed :
        feed.write(prefix)
        feed.write(delimiter.join([c for c in columns]))
        feed.write('\n')

        for d in iteminfo :
            try :
                values = [pmap[c](d) if c in pmap and pmap[c] is not None else '' for c in columns]
                feed.write(delimiter.join(values))
                feed.write('\n')
            except ValueError:
                continue

def __cid_url(url, 
    sitecode='sec', 
    channel='display',
    publisher='criteo',
    product='model',
    phase='event',
    campaign='monthlymedia',
    content_type='mobile',
    creative='20191101',
    segmentation='retartget') :
    uri = urlparse(url)
    _q = uri.query
    _q += '%scid=%s'%(
        '&' if 0<len(_q) else '?', 
        '_'.join([sitecode, channel, publisher, product, phase, campaign, content_type, creative, segmentation])
    )
    _f = '#%s'%(uri.fragment) if 0<len(uri.fragment) else ''
    return '%s://%s%s%s%s'%(uri.scheme, uri.netloc, uri.path, _q, _f)


def __build_cid_parser_fn(**kwargs) :
    def __cid_parser_fn(d) :
        return __cid_url(d['path'], product=d['model'], **kwargs)
    return __cid_parser_fn

def build_criteo_feed() :
    columns =(
        'id', 
        'title', 
        'description', 
        'availability', 
        'condition', 
        'price', 
        'link', 
        'link_mobile',
        'image_link', 
        'brand', 
        'additional_image_link', 
        'age_group', 
        'color', 
        'gender', 
        'item_group_id', 
        'gtin',
        'mpn',
        'google_product_category', 
        'material', 
        'pattern', 
        'product_type', 
        'sale_price', 
        'sale_price_effective_date', 
        'shipping', 
        'shipping_weight', 
        'size', 
        'custom_label_0', 
        'custom_label_1', 
        'custom_label_2', 
        'custom_label_3', 
        'custom_label_4')
    parsemap = {
        'link': __build_cid_parser_fn(
            channel='display',
            publisher='criteo', 
            phase='event',
            campaign='monthlymedia',
            content_type='desktop',
            creative='20191101',
            segmentation='retarget'),
        'link_mobile': __build_cid_parser_fn(
            channel='display',
            publisher='criteo',
            phase='event',
            campaign='monthlymedia',
            content_type='mobile',
            creative='20191101',
            segmentation='retarget'),
    }
    __build_text_feed('criteo.feed.txt', columns, parsemap=parsemap)
    
def build_google_feed() :
    columns = (
        # required
        'id',
        'title',
        'description',
        'link',
        'image_link',
        'availability',
        'price',
        'brand',
        # recommended
        'item_group_id',
        'loyalty_points',
        'gtin',
        'mpn',
        # optionals
        'sale_price',
        'product_type',
        'custom_label_0',
        'custom_label_1',
        'custom_label_2',
        'custom_label_3',
        'custom_label_4',
        'additional_image_link'
    )

    parsemap = {
        'price': __build_item_parse_price('%d KRW'),
        'sale_price': (lambda d: '%d KRW'%(d['sales']) if d['sales'] is not None else ''),
        'additional_image_link': __item_parsemap_additional_image ,
    }
    __build_text_feed('google.feed.txt', columns, parsemap=parsemap)


def build_facebook_feed() :
    columns = (
        # required
        'id',
        'title',
        'description',
        'availability',
        'condition',
        'price',
        'link',
        'image_link',
        'brand',
        # optional
        'additional_image_link',
        'age_group',
        'color',
        'gender',
        'item_group_id',
        'google_product_category',
        'material',
        'pattern',
        'product_type',
        'sale_price',
        'sale_price_effective_date',
        'shipping',
        'shipping_weight',
        'size',
        'custom_label_0',
        'custom_label_1',
        'custom_label_2',
        'custom_label_3',
        'custom_label_4' )
    parsemap = {
        'image_link': (lambda d: d['thumbnail_large'] if d['thumbnail_large'] is not None else d['thumbnail']),
        'link': __build_cid_parser_fn(
                channel='display',
                publisher='facebook', 
                phase='event',
                campaign='monthlymedia',
                content_type='mobile',
                creative='20191101',
                segmentation='retarget'),
        'price': __build_item_parse_price('%d KRW'),
        'sale_price': (lambda d: '%d KRW'%(d['sales']) if d['sales'] is not None else ''),
        'additional_image_link': __item_parsemap_additional_image,
        'item_group_id': (lambda d: ''),
     }
    __build_text_feed('facebook.feed.txt', columns, parsemap=parsemap)

if __name__ == '__main__' :
    import sys
    cmd = sys.argv[1]
    params = sys.argv[2:]
    cmd_map = {
        'migration': (lambda params: site.refresh_migrations(*params)),
        'category': (lambda params: check_categories(*params)),
        'item': (lambda params: check_category_items(*params)),
        '.items': (lambda params: _recent_items(*params)),      
        'feed': (lambda params: load_feed_data()),
        'google': (lambda params: build_google_feed()),
        'criteo': (lambda params: build_criteo_feed()),
        'facebook': (lambda params: build_facebook_feed()),
    }
    if cmd.lower() in cmd_map :
        cmd_map[cmd.lower()](params)


