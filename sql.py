#! -*- coding: utf8 -*-
import config       # config 디렉토리에 있는 것들 임포트
from . import cnx     # 현재 database폴더에서 cnx모듈을 가져옴
import mysql.connector
import math
import re
import json

from datetime import datetime, date, time

#__service_conf__ = config.service
#__conf__ = config.sql

connection_keys = (
    'user',
    'username',
    'password',
    'passwd',
    'host',
    'unix_socket',
    'port',
    'database',
    'auth_plugin',
    'use_unicode',
    'charset',
    'collation',
    'autocommit',
    #'time_zone',
    'pool_name',
    'pool_size',
    'failover',
)


default_kwargs = {
    'auth_plugin': 'mysql_native_password',
    'use_unicode': True,
    'charset': 'utf8mb4',
    #'time_zone': 'Asia/Seoul',
    'pool_name': config.service_name,
    'pool_size': int(math.ceil(config.workers*1.2)),
}


class connection(cnx) :                  # __init__.py의 cnx 클래스 상속받음
    def __init__(self, **cnf) :          
        super().__init__(**cnf)     
        self.__conf = cnf    # 자식 클래스에서 부모 클래스 내용을 사용하기 위해 super()  // __init__.py 의 __init__ 모듈 사용 self.__conf = config가 할당
        self.__cursor = None

    @property                        # 이 함수는 매소드 오버라이딩. (부모 config매소드를 재정의)
    def config(self, **configure) :  # configure를 받고, connection_keys값이 cnf에 있으면 defalut_kwargs.copy에 키와 값을 저장시킨다.
        cf = default_kwargs.copy()  
    
        for ck in connection_keys :
            if ck in self.__conf :                # 아마도 __init__ 된 __conf에 해당 키가 있다면 그값을 가져와서 cf에 추가
                cf[ck] = self.__conf[ck]
        return cf                           # cnf에서 connection_keys중 있는 키 값들을 deaflut_kwargs랑 합친 딕셔너리

    def init_connection(self) :                          # 초기 커넥션 만들기
        return mysql.connector.connect(**self.config)    # self.config는 뭘 뜻하는거임? 위에 함수 config? 변수 config는 없는거같은데?

    @property
    def cursor(self) -> mysql.connector.cursor : 
        if self.__cursor is None :                          
            self.__cursor = self.connection.cursor()   # __cursor가 처음에는 None 이엇으므로 새로운 커서를 할당해줌
        return self.__cursor

    def disconnect(self) :                  # has_connection이 없으면 연결을 종료한다. (__cnx이 None이면 종료)
        if not self.has_connection() :     ##단순히 이렇게 쓰면 부모클래스의 has_connection을 불러올수 있는건가? 그런가봄
            return

        try :
            self.cursor.close()
            self.connection.close()
        except :
            pass

    def exec(self, stmt:str, params) :                     #excute 구문
        return self.cursor.execute(stmt, params)
    
    def exec_many(self, stmt:str, params:list) :           #excute many 구문
        return self.cursor.executemany(stmt, params)

    def commit(self) :                                      
        self.connection.commit()                            #부모 commection 메소드에서 __cnF 불러와 커밋
        # refresh cursor
        self.cursor.close()                                 #커밋 후 커서 닫음
        self.__cursor = self.connection.cursor()            # 커서에 다시 커서 연결 시킴

    def __enter__(self) :                                   # with 문 진입시점에 바로 실행됨 (바로 커서 할당)         
        return self.cursor
    
    def __exit__(self, *args) :                             # with 문 종료직전에 바로 실행됨 (커밋 시킴)
        self.commit()

# build configured connections
(reader, writer) = connection.initiate(config.sql)    # 부모클래스의 initiate 모듈을 사용. @classmethod 적용되있어서 가능한듯
                                                      # config의 spl 값을 인자로 받는게 뭐지..?
# runner
READ_STMT_PATTERN = re.compile('^[\s\(]*SELECT ')  # 앞에 공백 포함해서 select로 시작하면...
def exec(stmt, params) :

    print(stmt, params)

    if READ_STMT_PATTERN.match(stmt) :    # select구문이면
        print(stmt)
        reader.exec(stmt, params)        # exec해서 읽어옴
    else :
        writer.exec(stmt, params)        # select 포함 안되있는 stmt면, writer.exec 실행

def exec_many(stmt, params:list) :
    writer.exec(stmt, params)

def result_iterator(connector=None) :
    connector = connector if connector is not None else reader
    return connector.cursor

# 
def iter_results(*parser, connector=None) :
    connector = connector if connector is not None else reader
  
    for row in connector.cursor :
        rs = tuple([parser[ci](cv) \
            if cv is not None and ci<len(parser) and parser[ci] is not None \
            else cv \
        for ci,cv in enumerate(row)])
        yield rs

def results(*parser, connector=None) :
    return [rs for rs in iter_results(*parser, connector=connector)]

def json_results(columns:tuple, connector=None, **parser) :
    connector = connector if connector is not None else reader
    pss = list(parser[cn] if cn in parser else None for cn in columns)

    rets = []
    for rs in iter_results(*pss, connector=connector) :
        rets.append({cn:rs[ci] for ci,cn in enumerate(columns)})
    return rets

def row_id(no_commit=False, connector=None) :
    connector = connector if connector is not None else writer
    if not no_commit :
        connector.commit()
    return connector.last_row_id

def commit(connector=writer) :
    connector = connector if connector is not None else writer
    connector.commit()

def close() :
    reader.disconnect()
    writer.disconnect()

def selects(table:str, columns='*', wheres:str='', orderby:str='', limits:int=-1, *params, **kwargs) :
    stmt = 'SELECT %s FROM %s'%(
        columns if isinstance(columns, str) else ','.join(str(c) for c in columns),
        table )

    if 0<len(kwargs) :
        keys = kwargs.keys()
        if 0<len(wheres) :
            wheres += ' AND '
        wheres += ' AND '.join(['(%s=%%s)'%(k) for k in keys])
        params += tuple(map(lambda k: kwargs[k], keys))
    if 0<len(wheres) :
        stmt += ' WHERE %s'%(wheres)
    if 0<len(orderby) :
        stmt += ' ORDER BY %s'%(orderby)
    if 0<limits :
        stmt += ' LIMIT %d'%(limits)
    print(stmt)
    # run query
    reader.exec(stmt, params)

    # parse results
    if isinstance(columns, str) and ',' not in columns :
        return results()
    elif isinstance(columns, str) :
        column_names = tuple(map(lambda cn: cn.strip(), columns.split(',')))
        return json_results(columns=column_names)
    else :
        return json_results(columns=columns)

def update(table:str, wheres:str, params:tuple, values:dict={}) :
    wh_keys = values.keys()
    stmt = 'UPDATE %s SET %s WHERE %s'%(
        table, 
        ','.join(['%s=%%s'%(vk) for vk in wh_keys]),
        wheres)
    # appending tuple
    params += tuple(map(lambda vk: values[vk], wh_keys))
    writer.exec(stmt, params)

def updates(table:str, wheres:list, params:tuple=([],[]), values:list=[]) :
    
    stmt = 'UPDATE %s SET %s WHERE %s'%(
        table, 
        ','.join(['%s=%%s'%(vk) for vk in values]),
        ' AND '.join(['%s=%%s'%(wh) for wh in wheres]))
    # appending tuple
    #params += tuple(map(lambda vk: values[vk], wh_keys))
    writer.exec_many(stmt, params)

def delete(table:str, wheres:str='', params:tuple=None, **kwargs) :
    if 0<len(kwargs) :
        if 0<len(wheres) :
            wheres += ' AND'
            params = tuple()
        vks = kwargs.keys()
        wheres += ' AND '.join(map(lambda k: '%s=%%s'%(k), vks))
        params += tuple(map(lambda k: kwargs[k], vks))
        
    stmt = 'DELETE FROM %s WHERE %s'%(table, wheres)
    writer.exec(stmt, params)

def _insert_stmt(table, keys) :
    return 'INSERT IGNORE  %s (%s) VALUES (%s)'%(
        table,
        ','.join(keys),
        ','.join(map(lambda k: '%s', keys))
    )


def insert(table:str, values:dict={}, **kwargs) :
    vs = values.copy()
    if 0<len(kwargs) :
        vs.update(**kwargs)
    
    vks = vs.keys()
    stmt = _insert_stmt(table, vks)
    params = tuple(map(lambda k: vs[k], vks))
    writer.exec(stmt, params)

def inserts(table:str, keys:tuple=(), values:list=[]) :
    stmt = _insert_stmt(table, keys)
    vs = values.copy()
    for ri, rv in enumerate(vs) :
        if isinstance(rv, dict) :
            vs[ri] = tuple([rv[k] if k in rv else None for k in keys])

    # filter
    for ri,rv in enumerate(vs) :
        puts = None
        for vi,vv in enumerate(rv) :
            if isinstance(vv, dict) : 
                if puts is None : puts = list(rv)
                puts[vi] = json.dumps(vv)
        if puts is not None :
            vs[ri] = tuple(puts)
                
    print(stmt)
    writer.exec_many(stmt, vs)


def _save_stmt(table, keys, index_keys) :
    #keys = #tuple(values.keys())
    vkeys = tuple(filter(lambda k: k not in index_keys))
    stmt = '''INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s'''%(
        table,
        ','.join(keys),
        ','.join(['%s' for k in keys]),
        ','.join(['%s=%%s'%(vk) for vk in vkeys])
    )
    print(stmt)
    print(vkeys)
    return (stmt, vkeys)

def _insert_update_stmt(table, keys, index_keys) :
    #keys = #tuple(values.keys())
    #vkeys = tuple(filter(lambda k: k not in index_keys))
    stmt = '''INSERT IGNORE %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s'''%(
        table,
        ','.join(keys),
        ','.join(['%s' for k in keys]),
        ','.join(['%s=%%s'%(vk) for vk in index_keys])
    )
    print(stmt)
    #print(index_keys)
    return (stmt)

def insert_update(table:str,keys:list,values:list):
    
    stmt = _insert_update_stmt(table,keys,keys)
    
    writer.exec_many(stmt, values)
    

def save(table:str, values:dict, index_keys:tuple=()) :
    keys = tuple(values.keys())
    vals = tuple(map(lambda k: values[k], keys))
    stmt, vkeys = _save_stmt(table, keys, index_keys)
    params = tuple(map(lambda k: values[k], keys + vkeys))

    writer.exec(stmt, params)

def saves(table:str, keys:tuple, index_keys:tuple, values:list) :
    stmt, vkeys = _save_stmt(table, keys, index_keys)
    params = []
    param_keys = keys + vkeys
    for val in values :
        params.append(tuple(map(lambda k: val[k] if k in val else None, param_keys)))
    
    writer.exec_many(stmt, params)
    
