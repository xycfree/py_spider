#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/18 10:47
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import threading
from Queue import Queue
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

queue = Queue()

class Producer(threading.Thread):
    def __init__(self, info):
        super(Producer, self).__init__()
        self.info = info

    def run(self):
        global queue
        try:
            while True:
                if self.info is not None:
                    if queue.qsize() > 1000:
                        pass
                    else:
                        queue.put(self.info)
                        print(self.info)
                        self.info = None
                    time.sleep(0.01)
                else:
                    break
        except Exception, e:
            raise str(e)

class Consumer(threading.Thread):
    def __init__(self):
        super(Consumer,self).__init__()

    def run(self):
        global queue
        while True:
            if queue.qsize() == 0:
                pass
            else:
                info = queue.get()
                print(info)
            time.sleep(0.01)





