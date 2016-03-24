# -*- coding: utf-8 -*-
"""
bottle baseapp framework sample
"""

# bottle framework
from bottle import Bottle
from bottle import static_file
from bottle import request
from bottle import response
from bottle import SimpleTemplate
from bottle import BaseRequest

import traceback
import json

# built in function
import importlib
import os
import copy
import re

# main class of framework
class BaseApp(Bottle):
    def __init__(self):
        Bottle.__init__(self)
        
        # set default configuration
        self.__set_default_configuration()
        
        # set max mem body request
        BaseRequest.MEMFILE_MAX = self.config['memfile_max']
        
        # set configuration
        self.set_configuration()
        
        # call default route
        # register default route
        self.__set_default_route()
        
        # set view
        self.set_view()
        
        # call route
        # register route
        self.set_route()
        
        # uri param
        # if call using module/action/method/param/value/param/value/paramN.../valueN...
        self.__uri_param = {}

        # init session check and thread sessino check
        self.session = Session(self)
        self.session_thread = Thread(target=self.session.cleanup_session_file)
        self.session_thread.setDaemon(True)
        self.session_thread.start()

    def get_uri_param(self):
        return self.__uri_param
    
    def res(self):
        return response
        
    def req(self):
        return request
    
    # set default configuration
    def __set_default_configuration(self):
        # add config
        
        # configuration for running service
        self.config['ip_address'] = '127.0.0.1'
        self.config['port'] = 8888
        self.config['reloader'] = False
        self.config['interval'] = 1
        self.config['page_url'] = ''
        self.config['template'] = 'default'
        self.config['memfile_max'] = 10*1024*1024 #10MB
        
    # init view
    def set_view(self):
        # global template path
        # path global view under apps
        tpl_views_folder = r''  + os.path.sep.join((os.getcwd(), 'views', self.config.get('template'))) + os.path.sep
        self.config['views_path'] = tpl_views_folder
    
    # configuration
    # should override for new implementation
    def set_configuration(self):
        # this implementation depend on developer implementation
        pass
     
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
        self.redirect(self.config['page_url'])
        
    # register default route
    def __set_default_route(self):
        # default page url
        self.route(path='/', method='GET', callback=self.__default_page, name='default_page')
    
        # basic framwork route
        self.route(path='/p/<uri:path>', method='GET', callback=self.parse_request, name='parse_get')
        self.route(path='/p/<uri:path>', method='POST', callback=self.parse_request, name='parse_post')
        self.route(path='/<filepath:path>', method='GET', callback=self.serve_static, name='static_get')
        
    # register route
    # create custrom route is okay!
    # this should be override with new implementation
    def set_route(self):
        # this implementation depend on developer implementation
        pass
    
    # parse callback
    # module is module name
    # action is action name
    # index is default value
    # if method not defined then call default module action method index
    def parse_request(self, uri):
        # uri[0] is module name
        # uri[1] is action name
        # uri[2] is method name
        uri = uri.split('/') # split uri
        module = uri[0]
        action = uri[1]
        method = 'index'
        if len(uri) >= 3:
            method = uri[2] # set method if uri call method is set
            
        # if uri length more than 3
        # set to get param
        # /module/action/method/param/value/param/value/param/value/paramN.../valueN...
        self.__uri_param = {}
        if len(uri) > 3:
            gparam = '/'.join(uri[3:])
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
                
        try:
            # set active modules call path
            # this path is used when call template file
            tpl_views_folder = r'' + os.path.sep.join((os.getcwd(), 'modules', module, 'views'))
            self.config['module_views_path'] = ''.join((tpl_views_folder, os.path.sep))

            action_path = '.'.join(('modules', module, action))
            module_action_file = r'' + os.path.sep.join((os.getcwd(), 'modules', module, ''.join((action, '.py'))))
            
            if os.path.isfile(module_action_file):
                
                # call action module
                module_action = importlib.import_module(action_path)
                module_action = importlib.reload(module_action)
                module_action = getattr(module_action, action[0].upper() + action[1:])
                module_action = module_action(app=self)
                
                call_method = getattr(module_action, method)
                return call_method()
                
            else:
                return None
                
        except Exception:
            pass
            print(traceback.format_exc())
            return json.dumps({'error':repr(traceback.format_exc())})
        
    def get_template_path(self, template_name):
        '''
            return template path
            should be nested under template name
            site.header
        '''
        template_name = self.to_path(template_name, absolute=False)
        return ''.join((self.config.get('views_path'), template_name, '.html'))
    
    def to_path(self, dot_path, absolute=True):
        '''
            convert .path to os path
            ex unix views.sikilku.com
            will convert to views/sikilku/com
            if absolute=False will return without os.getcwd()
            getcwd means your app location path
        '''
        dot_path = dot_path.replace('.', os.path.sep)
        # default
        if absolute:
            return os.path.sep.join((os.getcwd(), dot_path))
        
        # non absolute path
        return dot_path
    
    # render template
    # template name
    # template name should be end with .tpl
    # call template must be using
    # appviews.template_name => this is for view under apps/views
    # views.template_name => this is for view under modules_name/views
    def render(self, template_name, param=None):
        try:
            # read template file
            # validate if template path exist
            template_name = self.to_path(template_name, absolute=False)
            tpl_path = r'' + ''.join((self.config.get('views_path'), template_name, '.html'))
            
            # setup param data    
            param_data = {}
            
            if param:
                param_data = param
                
            # make available to include other view from appview and module view
            param_data['app'] = self
            
            # read template file
            if os.path.isfile(tpl_path):
                tpl_file = open(tpl_path)
                tpl_content = ''.join(tpl_file.readlines())
                tpl_file.close()
                
                # return parsed template
                return SimpleTemplate(tpl_content).render(data=param_data)
            
            # if tpl file not found
            else:
                return 'Template file not found ' + template_name
                
        except Exception:
            print(traceback.format_exc())
            return json.dumps({'error':repr(traceback.format_exc())})
        
    # server static file under apps/static folder
    # access through http://yoursite/p/statics/[folder_under_static]/[..]/[..]/filename.xyz
    def serve_static(self, filepath):
        return static_file(filepath, root=''.join((os.getcwd(),)))
        
