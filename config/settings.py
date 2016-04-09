# -*- coding: utf-8 -*-

import os
import logging
from sys import argv
import libs.environment

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = path(ROOT, '../statics')
TEMPLATE_ROOT = path(ROOT, '../templates')  # not used
TEMP_ROOT = path(ROOT, '../run/tmp')
UGC_PATH = path(ROOT, '../run/ugc')
LOG_PATH = path(ROOT, '../run/logs')

# Deployment Configuration
class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    dict = {
        PRODUCTION: 1,
        DEV: 2
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.DEV

settings = {}
# 以下配置项目根据运行环境的不同灵活配置
if DEPLOYMENT==DeploymentType.PRODUCTION:
    settings["debug"] = False
    settings["db_cfg"] = {
        "dbhost":"127.0.0.1",
        "dbport": 3306,
        "dbuser":"user",
        "dbpass":"pass",
        "dbname":"db",
        "socket": '/data/mysqldb/mysql.sock',
        "dbchar":"utf8"
                        }
    settings["im_cfg"] = {}

else:
    settings["debug"] = True
    settings["db_cfg"] = {
        "dbhost":"127.0.0.1",
        "dbport": 3306,
        "dbuser":"user",
        "dbpass":"pass",
        "dbname":"db",
        "socket": 'F:\\srv\\mysql-5.5.28-winx64\\data\\mysql.sock',
        "dbchar":"utf8"
                        }
    settings["im_cfg"] = {}


# 以下参数为应用的系统级参数， 禁止修改
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "481da2252edca50d9f4cc8a01b40ac61meetingadmin"
settings['xsrf_cookies'] = True
settings['domain'] = 'http://127.0.0.1:5000'
#请求、响应参数加密密钥
settings["key_network_out"] = "d]e$123sh$1123%an^g["    #request
settings["key_network_in"] = "d!#@]e$VSshW%an^g["       #response
#memcached settings
settings['memcached_address'] = ["127.0.0.1:11211"]

settings['memcached_expire_table'] = {
}

#临时目录
settings['temp_dir'] = TEMP_ROOT
#ugc目录
settings["ugc"] = UGC_PATH

#logging
#settings['debug'] = options.debug
#settings['log_level'] = options.log
settings['logging_config'] = { "log_level":logging.INFO, \
                             "log_format":"%(asctime)s %(levelname)s [%(lineno)04d] >>>> %(message)s", \
                             "log_name":"log",  \
                             "log_path":LOG_PATH}
