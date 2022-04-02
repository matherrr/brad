#! -*- coding: utf8 -*-

from datetime import datetime

def timelog(content) :
    print('[%s] %s'%(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        str(content)
    ))