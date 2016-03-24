# -*- coding: utf-8 -*-
"""
应用基础类
"""
# bottle framework
from bottle import Bottle
from bottle import static_file
from bottle import request
from bottle import response
from bottle import SimpleTemplate
from bottle import BaseRequest

import sys
import gevent
import bottle
import ssl
import time
import traceback
import json
# import configparser

# built in function
import importlib
import os
import copy
import re

from json import loads, dumps
from random import random
from datetime import datetime, timedelta, date
import re


# main class of framework
class Application(Bottle):
    def __init__(self, settings = None):
        Bottle.__init__(self)

        # bytes, 设为5M
        BaseRequest.MEMFILE_MAX = 5 * 1024 * 1024
        
        #self.settings = settings or {}
        self.settings = settings

        reload(sys)
        sys.setdefaultencoding('utf8')
        ssl._create_default_https_context = ssl._create_unverified_context

        if not self.init_logger():
            print "failed to init logger,please check whether the logger info configured in config.py"
            sys.exit()
        else:
            self.logger.info("logger init succeed.")

        import urllib3
        urllib3.disable_warnings()
        self.http_pool = urllib3.PoolManager(5, maxsize=5000, block=True)
        
        from dbutil import Mysql
        self.db = Mysql(self.settings["db_cfg"])

        import memcache
        self.mc = memcache.Client(self.settings["memcached_address"])

        # call default route
        # register default route
        self.__set_default_route()

        # add hook for all
        self.add_hook("before_request", self.hook_before_request)

        # uri param
        # if call using module/action/method/param/value/param/value/paramN.../valueN...
        self.__uri_param = {}

    '''
    before request hook中处理静态文件请求
    '''
    def hook_before_request(self):
        if bottle.request.environ['PATH_INFO'] == '/error':
            return
        try:
            pathinfo = bottle.request.environ['PATH_INFO']
            s = os.path.sep.join(pathinfo.rstrip('/').lstrip('/').split('/'))
            s = os.path.sep.join((os.getcwd(), 'statics', s))
            # print('=> %s '%s)
            # 如果该文件存在，直接路由该文件为静态文件
            if os.path.exists(s):
                self.route(path=pathinfo, method='GET', callback=self.serve_static2, name='static_get')

    	except Exception, e:
    		self.logger.error(e)
    		#raise error.AppException(error.ERR_LIST_EMPTY, 'ptlogin failed')

    # server static file under apps/static folder
    # access through http://yoursite/p/statics/[folder_under_static]/[..]/[..]/filename.xyz
    def serve_static2(self):
        return static_file(bottle.request.environ['PATH_INFO'], root=os.path.sep.join((os.getcwd(),'statics')))


    def init_logger(self):
        try:
            import logging
            import logging.handlers
            import time
            import os

            self.logger = logging.getLogger("%s.%s" % (self.settings["logging_config"]["log_name"], time.time()))
            # 类似nginx日志，按时间每天一个文件，其他回滚另议
            file_path = os.path.realpath("%s/%s-%s.log" % (self.settings["logging_config"]["log_path"], self.settings["logging_config"]["log_name"], time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())))
            # print file_path
            file_handler = logging.handlers.TimedRotatingFileHandler(file_path,when='D',interval=1, backupCount=31)
            file_handler.suffix = self.settings["logging_config"]["log_name"] + '-' +  time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".log"
            file_handler.setLevel(self.settings["logging_config"]["log_level"])
            file_handler.setFormatter(logging.Formatter(self.settings["logging_config"]["log_format"]))
            self.logger.addHandler(file_handler)
            return True
        except Exception, e:
            print traceback.format_exc()
            return False

    def get_uri_param(self):
        return self.__uri_param

    def res(self):
        return response

    def req(self):
        return request


    # get base path location
    def get_base_dir(self):
        return ''.join((r'', os.getcwd(), os.path.sep))

    # get static path folder
    def get_statics_path_dir(self):
        return ''.join((r'', os.getcwd(), os.path.sep, 'statics', os.path.sep))

    # get base url
    # will return base url http://yourdomain.com:port
    def get_base_url(self):
        url_part = self.req().urlparts
        return ''.join((url_part.scheme, '://', url_part.netloc))

    # redirect url
    def redirect(self, url):
        self.res().status = 303
        return self.res().set_header('Location', url)

    # goto default url
    def __default_page(self):
        # self.redirect(self.config['page_url'])
        pass

    # register default route
    def __set_default_route(self):
        # default page url
        # self.route(path='/', method='GET', callback=self.__default_page, name='default_page')

        # basic framwork route
        self.route(path='/api/<uri:path>', method='GET', callback=self.parse_request, name='parse_get')
        self.route(path='/api/<uri:path>', method='POST', callback=self.parse_request, name='parse_post')
        self.route(path='/<filepath:path>', method='GET', callback=self.serve_static, name='static_get')

    # parse callback
    # module is module name
    # action is action name, index is default
    def parse_request(self, uri):
        # uri[0] is module name
        # uri[1] is action name

        uri = uri.rstrip('/').split('/') # split uri
        module = uri[0]
        action = 'index'
        if len(uri) >= 2:
            action = uri[1] # set method if uri call method is set

        print(" module => %s, action => %s "%(module, action))

        # if uri length more than 2
        # set to get param
        # /module/action/param/value/param/value/param/value/paramN.../valueN...
        self.__uri_param = {}
        if len(uri) > 2:
            gparam = '/'.join(uri[2:])
            gparam = re.sub('(/+)', '/', gparam)
            if gparam[0] == '/':
                gparam = gparam[1:]
            if gparam[-1] == '/':
                gparam = gparam[:-1]

            gparam = gparam.split('/')
            len_gparam = len(gparam)
            xparam = len_gparam%2
            # mean param value in the end of uri is empty
            if xparam:
                len_gparam -= 1
                self.__uri_param[gparam.pop(len_gparam - 1)] = None

            for index in range(0, len_gparam, 2):
                self.__uri_param[gparam[index]] = gparam[index + 1]

        # print(" module => %s, action => %s "%(module, action))

        try:
            # set active modules call path
            action_path = '.'.join(('modules', module))
            module_action_file = r'' + os.path.sep.join((os.getcwd(), 'modules', ''.join((module, '.py'))))
            # print(" => %s "%action_path)
            # print(" => %s "%module_action_file)

            if os.path.isfile(module_action_file):
                # call action module
                module_action = importlib.import_module(action_path)
                # module_action = importlib.reload(module_action)
                module_action = getattr(module_action, module[0].upper() + module[1:])
                module_action = module_action(app=self)

                call_action = getattr(module_action, action)
                return call_action()
            else:
                # print(" => Error: no module named %s"%action_path)
                return None

        except Exception:
            pass
            print(traceback.format_exc())
            return json.dumps({'error':repr(traceback.format_exc())})

    # server static file under apps/static folder
    # access through http://yoursite/p/statics/[folder_under_static]/[..]/[..]/filename.xyz
    def serve_static(self, filepath):
        print('=> %s '%os.path.sep.join((os.getcwd(),'statics')))
        print('=> %s '%filepath)
        return static_file(filepath, root=os.path.sep.join((os.getcwd(),'statics')))

    def __default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            raise TypeError('%r is not JSON serializable' % obj)

    """
    json_encode      creates a json string or jsonp string
    """
    def json_encode(self, data, callback=''):
        res = dumps(data, default=self.__default)
        if callback == None or callback == '':
            return res
        else:
            return '%s(%s)' % (callback, res)

    """
    json_decode      explode a json to or other datatype
    """
    def json_decode(self, data):
        if not data:
            return data
        else:
            return loads(data)

    def return_data(self, result=0,massage='',data=''):
        res={}
        res['result']=result
        res['msg']=massage
        res['data']=data
        return res



