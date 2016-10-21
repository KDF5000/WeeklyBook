#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time, logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import os
from SMTPClient import SMTPClient,Message

EXT_LIST = ['mobi'] #可以添加azw3, epub 等任何格式
HOST_NAME = 'smtp.cstnet.cn'
HOST_PORT = 25
USER_NAME = 'kongdefei@ict.ac.cn'
USER_PASS = 'kong19920213'
KINDLE_MAILS = ['kdf5000@kindle.cn'] #可以为一个list
FROM_NAME = 'kongdefei@ict.ac.cn'
TO_NAME = 'Kindle'

class FileSyncEvent(FileSystemEventHandler):

    def __init__(self):
        self._logger = logging.getLogger('server')

    def on_created(self, event):
        # print type(event)
        created_file = os.path.abspath(event.src_path)
        self._logger.info("Create file %s"%created_file)

        ext_name = os.path.splitext(created_file)[1]
        if ext_name in ['.mobi']:
            self._logger.info("Send to kindle %s..."%created_file)
            send_to_kindle(created_file)
        
    
    def on_modified(self,event):
        # print type(event)
        self._logger.info("Modify file %s"%event.src_path)

def send_to_kindle(file):
    logger = logging.getLogger("SendToKindle")
    smpt_client = SMTPClient(HOST_NAME,HOST_PORT,USER_NAME,USER_PASS)
    msg = Message(FROM_NAME,TO_NAME,'Daily EBook','Daily EBook from KDF5000, Thanks!',with_attach=True)
    msg.attach(file)
    # print msg.getMessage()
    res, msg = smpt_client.send(USER_NAME,KINDLE_MAILS,msg)
    if res == 1:
        logger.info("Send %s to kindle successfully!"%file)
    else:
        logger.error(msg)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("Main")
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileSyncEvent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    logger.info("Start sync server")
    observer.start()
    logger.info("Begin to mornitor!")
    try:
        while True:
           time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
