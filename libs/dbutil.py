# -*- coding: UTF-8 -*-
"""
desc: MySQLDB Operation
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

"""
Config: DB configuration file
"""

class Mysql(object):
    """
        MYSQL db class，for db connection management, using connection pool
        get connection: conn = Mysql.getConn()
        release connection: conn.close()或del conn
    """
    #poll obj
    __pool = None
    def __init__(self, dbsetting):
        """
        constructor: get connection resource from pool，and generate cursor
        """
#        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
#                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = Mysql.__getConn(dbsetting)
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(dbsetting):
        """
        @summary: static method，get connection resource from pool
        @return MySQLdb.connection
        """
        print(dbsetting)
        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,
                              host=dbsetting['dbhost'] , port=dbsetting['dbport'] , user=dbsetting['dbuser'] , passwd=dbsetting['dbpass'] ,
                              db=dbsetting['dbname'],use_unicode=False,charset=dbsetting['dbchar'],unix_socket=dbsetting['socket'],cursorclass=DictCursor)
        return __pool.connection()

    def query(self,sql,param=None):
        """
        @summary: execute non-select operation insert update delete
        @param sql: SQL
        @param param: optional，condition（tuple/list）
        @return: result count
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        self._conn.commit()
        return count

    def getCount(self,sql):
        count = self._cursor.execute(sql)
        if count > 0:
            return (self._cursor.fetchall())[0]['count(*)']
        else:
            return 0

    def last_insert_id(self):
        return self._cursor.lastrowid

    def getAll(self,sql,param=None):
        """
        @summary: execute and get all result records
        @param sql:SQL, mostly select operation
        @param param: optional，condition（tuple/list）
        @return: result list/boolean
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchall()
            self._conn.commit()
        else:
            result = False
        return result

    def getOne(self,sql,param=None):
        """
        @summary: execute and get the first record
        @param sql: SQL
        @param param: optional，condition（tuple/list）
        @return: result list/boolean
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchone()
            self._conn.commit()
        else:
            result = False
        return result

    def begin(self):
        """
        @summary: start of transaction
        """
        self._conn.autocommit(0)

    def end(self,option='commit'):
        """
        @summary: end of transaction
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self,isEnd=1):
        """
        @summary: release connection pool
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()

"""
desc: Memcache Operation
"""
class MemcacheUtil(object):
    def __init__(self, mc = None):
        # set memcache client API
        self.mc = mc 

    def get_memcached_value(self, key):
        if self.mc: 
            value = self.mc.get(key)
            if value:
                decodedvalue = self.json_decode(value)
                return decodedvalue
        return None
    
    def set_memcached_value(self, key, value, expire):
        if self.mc: 
            encodedvalue = self.json_encode(value)
            self.mc.set(key, encodedvalue, expire)
            
    def delete_memcached_value(self, key):
        if self.mc: 
            self.mc.delete(key)
            
    def delete_multi_memcached_value(self, keys, key_prefix=''):
        if self.mc and not self.settings['debug']: 
            self.mc.delete_multi(keys, 0, key_prefix)
        


