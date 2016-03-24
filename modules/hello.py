# -*- coding: utf-8 -*-
#  modules 目录下实现业务逻辑处理（controller）和存储层数据获取（model）

import bottle
import time
import gevent
import re

class Hello():

    # init action constructor
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.mc = app.mc
        self.memcached_expire_table = app.settings['memcached_expire_table']
            
    # jsonp api
    def display(self):
        c = bottle.request.params.get('callback', None)
        p = bottle.request.params.get('p', 0)
        params = dict()
        if p:
            params = self.app.json_decode(p)
            
        req = params['req'] if params.has_key('req') else ''
        # handle request message
        rs = func(req)
        res = dict()
        if not rs:
            res = self.app.return_data(-2, "no data", {})
        else:
            res = self.app.return_data(1, "succ", rs)
        return self.app.json_encode(res, c)

