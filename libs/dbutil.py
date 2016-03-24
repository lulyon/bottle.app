# -*- coding: UTF-8 -*-
"""
desc:数据库操作类
@note:
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

"""
Config是一些数据库的配置文件
"""

class Mysql(object):
    """
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
        获取连接对象：conn = Mysql.getConn()
        释放连接对象;conn.close()或del conn
    """
    #连接池对象
    __pool = None
    def __init__(self, dbsetting):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
#        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
#                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = Mysql.__getConn(dbsetting)
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(dbsetting):
        """
        @summary: 静态方法，从连接池中取出连接
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
        @summary: 执行非查询操作 insert update delete
        @param sql:ＳＱＬ语句，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result count 受影响的行数
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
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
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
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
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
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self,option='commit'):
        """
        @summary: 结束事务
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()


class MemcacheUtil(object):
    def __init__(self, mc = None):
        # 设置 memcache client API
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
        


