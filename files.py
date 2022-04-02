#!
import re
import os.path
from datetime import datetime

from dbproj.database.sql import connector as db

class builder :
    __PATH__ = os.path.abspath('./output')
    def __init__(self, name, columns=[], encoding='euc-kr') :
        self._name = name
        self._columns = columns

        self.extension = 'csv'
        self.encoding = encoding

        self.parsers = []
        self.data = []

    def write(self, delimiter=',', linefeed='\n') :
        def cellvalue(col,ci,row) :
            cell = str(col) if col is not None else ''
            if ci in self.parsers and self.parsers[ci] is not None :
                fn = self.parsers[ci]
                cell = fn(col,ci,row)
            elif self._columns[ci] in row:
                cell = row[self._columns[ci]]

            if delimiter in cell or linefeed in cell :
                cell = '"%s"'%(cell.replace('"', r'\"'))

            return cell
        path = os.path.join(self.folder, self.filename)
        
        with open(path, mode='w', encoding=self.encoding) as fp :

            # write header
            fp.write(delimiter.join(self.columns))
            fp.write(linefeed)

            for row in self.data :
                line = delimiter.join([cellvalue(col,ci,row) for ci,col in enumerate(row)])
                fp.write(line)
                fp.write(linefeed)

        return path     

    @property
    def folder(self) :
        now = datetime.now()
        folder = os.path.join(self.__PATH__, '%4d'%(now.year),'%02d'%(now.month),'%02d'%(now.day),'%02d'%(now.hour))
        if not os.path.exists(folder) :
            os.makedirs(folder)
        return folder


    @property
    def filename(self) :
        return '%s.%s'%(self._name, self.extension.lower())

    @property
    def columns(self) :
        return self._columns
    

def nosp(days_before=7, until_day=None) :
    columns = ('일자','유형','캠페인','디바이스','광고상품','키워드','광고소재요소','노출수','클릭수','익스텐션클릭수','광고비','CPM','CPC','CTR')

    product_pattern = re.compile(r'^(?P<device>P|M)_(?P<type>[^_]+)(_(?P<detail>.+))?$')
    device_types = {'M': '모바일', 'P': 'PC'}
    def parse_pattern(ad_product) :
        match = product_pattern.match(ad_product)
        if match is not None :
            _v = match.group('device')
            v = device_types[_v.upper()[0]]
            t = match.group('type')
            d = match.group('detail')

            return (v,t,d if d is not None else '')

    def fetch_row(row) :
        (campaign_id, day_id, prod, brand, kw, grp, imps, clks, costs) = row
        imps = int(imps)
        clks = int(clks)
        costs = int(costs)
        device,adtype,detail = parse_pattern(prod)
        return (
            day_id,
            adtype,
            brand,
            device, 
            prod,
            kw,
            grp,
            imps,
            clks,
            0,
            costs,
            '%.2f'%((costs*1e3)/imps) if 0<imps else '-',
            '%.2f'%(1e0*costs/clks) if 0<clks else '-',
            '%.2f'%(1e0*clks/imps) if 0<imps else '-',
        )

    until_day = until_day if until_day is not None else datetime.today().date().isoformat()
    db.exec('''SELECT 
        c.id, r.day_id, r.ad_product, c.brand, r.ad_keyword, r.ad_group, SUM(r.impressions), SUM(r.clicks), SUM(r.cost)
        FROM campaign_records r JOIN campaigns c ON c.id=r.campaign_id
        WHERE 
            c.ad_channel = %s AND c.ad_type = %s
            AND r.day_id <= %s AND %s - INTERVAL %s DAY <= r.day_id
        GROUP BY c.id, r.day_id, r.ad_product, c.brand, r.ad_keyword, r.ad_group 
        ORDER BY c.id, r.day_id''', ('naver','display', until_day, until_day, days_before))
    bld = builder('NOSP', columns)
    bld.data = list(map(fetch_row, db.results()))
    bld.write()
    

def daum(days_before=7, until_day=None) :
    columns = (
        '광고주',
        '대행사',
        '브랜드',
        '캠페인',
        '날짜',
        '광고그룹',
        '키워드',
        '노출수',
        '클릭수',
        '광고비',
        'CPM',
        'CPC',
        'CTR')
    until_day = until_day if until_day is not None else datetime.today().date().isoformat()

    def fetch_row(row) :
        (campaign_id, account, agency, campaign, day_id, kw, imps, clks, costs) = row
        imps = int(imps)
        clks = int(clks)
        costs = int(costs)
        return (
            account,
            agency,
            campaign,
            str(day_id),
            kw,
            imps,
            clks,
            costs,
            '%.2f'%((costs*1e3)/imps) if 0<imps else '-',
            '%.2f'%(1e0*costs/clks) if 0<clks else '-',
            '%.2f'%(1e0*clks/imps) if 0<imps else '-',
        )
    
    db.exec('''SELECT
        c.id, c.account, c.agency, c.title, r.day_id, r.ad_keyword, r.impressions, r.clicks, r.cost
        FROM campaign_records r JOIN campaigns c ON c.id=r.campaign_id
        WHERE c.ad_channel = %s AND c.ad_type = %s
            AND r.day_id <= %s AND %s - INTERVAL %s DAY <= r.day_id
        ORDER BY c.id, r.day_id''', ('daum','search', until_day, until_day, days_before))
    bld = builder('DAUM', columns)
    bld.data = list(map(fetch_row, db.results()))
    bld.write()


def adobe(days_before=15, until_day=None) :
    columns = (
        '사이트',
        '채널카테고리',
        '채널유형',
        '일자',
        '매체',
        '품목',
        '캠페인',
        '크리에이티브',
        '세그먼트',
        'Visit',
        'CartAdd',
        'Order',
        'Revenue',
        'Bounces',
        'Entries',
        'Cancels',
        'Canceled Revenues',
        'Total Seconds')
    until_day = until_day if until_day is not None else datetime.today().date().isoformat()

    cid_options = ('site','channel_category','channel_type','publisher','product','phase','campaign','content_type','creative','segmentation')
    def parse_cid(cid:str) :
        tokens = cid.split('_')
        return {opt: tokens[oi] if oi<len(tokens) and tokens[oi] is not None else '' for oi,opt in enumerate(cid_options)}

    def fetch_row(row) :
        (cid,day,visits,carts,orders,revenue,bounces,entries,cancels,cancel_rev,duration) = row
        cid = parse_cid(cid)
        
        return (
            cid['site'],
            cid['channel_category'],
            cid['channel_type'],
            day,
            cid['publisher'],
            cid['product'],
            cid['campaign'],
            cid['creative'],
            cid['segmentation'],
            int(visits) if visits is not None else 0,
            int(carts) if carts is not None else 0,
            int(orders) if orders is not None else 0,
            int(revenue) if revenue is not None else 0,
            int(bounces) if bounces is not None else 0,
            int(entries) if entries is not None else 0,
            int(cancels) if cancels is not None else 0,
            int(cancel_rev) if cancel_rev is not None else 0,
            float(duration) if duration is not None else 0.0,
        )


    db.exec('''SELECT
        sid, day_id, visits, stats->"$.cart_add", conversions, value, stats->"$.bounces", stats->"$.entries", stats->"$.cancels", stats->"$.cancel_value", stats->"$.secondes"
        FROM segment_performances WHERE day_id <= %s AND %s - INTERVAL %s DAY <= day_id''', (until_day, until_day, days_before))

    bld = builder('ADOBE', columns)
    bld.data = list(map(fetch_row, db.results()))
    bld.write()


if __name__ == '__main__' :
    adobe()
    nosp()
    daum()