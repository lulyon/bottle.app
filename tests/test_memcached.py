# -*- coding: utf-8 -*-

import unittest
import memcache
import time

class MyTestCase(unittest.TestCase):
    def test_something(self):
        # self.session_manager = SessionManager(settings["session_secret"], settings["memcached_address"], settings["session_timeout"])

        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set('test_key1', 'value1')
        mc.set('test_key2', 'value2', 3)
        time.sleep(4)
        v1 = mc.get('test_key1')
        v2 = mc.get('test_key2')
        # 超时后， get得到的值为None
        self.assertIsNone(v2)
        self.assertEquals(v1, 'value1')
        # 删除后， 值为Nonoe
        mc.delete('test_key1')
        v1 = mc.get('test_key1')
        self.assertIsNone(v1)

    def get_current_session(self):
        """
        Return the request's session object.
        can be called using BaseHandler self.get_current_session() or
        by get_current_session(request_handler_instance)
        """
        # loads the session if have a session cookie and have a session key in sessions. else None
        session = sessions.get('abcdefg')

        # creats a new session incase there isn't one or if requested session expired
        if not session or session['expires'] < datetime.now():
            id = str(abs(hash(random())))
            self.set_cookie('session', id)
            sessions[id] = session = {'data': {}}
        # prolongs session expire time with session_expire or the default 20 minutes
        session['expires'] = datetime.now() + timedelta(minutes=self.application.settings.get('session_expire', 20))
        return session['data']

if __name__ == '__main__':
    unittest.main()
