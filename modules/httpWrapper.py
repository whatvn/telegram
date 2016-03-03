
from gevent.pywsgi import WSGIServer
import gevent.monkey
import gevent
import api
from app import app
from multiprocessing import Process, current_process
import logging
import os
import sys

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_all()



__version__ = "Simplest HTTP Server/v0.1"
PROCESSES = []
logger = logging.getLogger()

def setup_logging(logfile, verbose, work_dir):
    log_path = os.path.join(work_dir, 'log')
    logger.setLevel(logging.DEBUG)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    formatter = logging.Formatter('%(asctime)-15s (%(name)s) %(message)s')
    log_level = logging.DEBUG if verbose else logging.INFO

    if logfile:
        logfile = os.path.join(log_path, logfile)
        file_log = logging.handlers.TimedRotatingFileHandler(
            logfile,
            when="midnight",
            backupCount=31)
        file_log.setLevel(log_level)
        file_log.setFormatter(formatter)
        logger.addHandler(file_log)


class HTTPServer(object):
    """
    A simple http wrapper
    """
    def __init__(self, host, port, processes, logfile, verbose, work_dir):
        self.host = host
        self.port = port
        self.processes = processes
        self.logfile = logfile
        self.verbose = verbose
        self.work_dir = work_dir
        setup_logging(self.logfile, self.verbose, self.work_dir)
        self.server = WSGIServer((self.host, self.port), app, backlog=100000, log=logger)
        self.server.init_socket()

    def serve_forever(self):
        self.server.start_accepting()
        self.server._stop_event.wait()
        gevent.wait()

    def start(self):
        for i in range(self.processes):
            p = Process(target=self.serve_forever, args=tuple())
            p.start()
            PROCESSES.append(p)
        try:
            print "Start listener"
            for p in PROCESSES:
                p.join()
        except KeyboardInterrupt:
            for p in PROCESSES:
                print "stopping %s" % p.name
                p.terminate()
        except:
            pass
        finally:
            print "Done"
            sys.exit(0)


