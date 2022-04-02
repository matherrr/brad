import config
from . import cnx
import redis
import re
import json

connection_keys = (
    'host',
    'port',
    'db',
    'password',
    'encoding',
    'decode_responses',   
)

default_conf = {
    'encoding': 'utf8',
    'decode_responses': True,
}

class __cnx(cnx) :
    def __init__(self, **conf) :
        super().__init__(**conf)
        self.__pipe = None


    @property
    def config(self, **conf):
        cf = default_conf.copy()
        for ck in connection_keys :
            if ck in self.__conf :
                cf[ck] = self.__conf[ck]
        return cf

    def init_connection(self) :
        pool = redis.ConnectionPool(max_connections=int(2*config.workers), **self.config)
        return redis.Redis(connection_pool=pool)
        
    def disconnect(self) :
        if self.has_connection() :
            self.connection.close()
    
    def __enter__(self) :
        return self.pipe()
    
    def __exit__(self, *args) :
        return self.__pipe.execute()

    def pipe(self) :
        self.__pipe = self.connection.pipeline()
        return self.__pipe

(reader, writer) = __cnx.initiate(config.redis)
connector = writer.connection







