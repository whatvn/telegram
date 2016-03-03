#!/usr/bin/env python

import optparse
from  modules import httpwrapper
from multiprocessing import cpu_count
from modules.api import TelegramBot, MsgSender
from modules.app import queue

# Telegram bot api token
TELEGRAM_TOKEN = ''

def main():

    parser = optparse.OptionParser()
    parser.add_option(
        '-i', '--host', dest='host', default='0.0.0.0',
        help='Hostname or IP address. Default is 0.0.0.0'
        )
    parser.add_option(
        '-p', '--port', dest='port', type='int', default=2001,
        help='Port. Default is 2000')
    parser.add_option(
        '-P', '--processs', dest='number_of_processes', type='int', default=1,
        help='Number of children to prefork. Default is 10')
    parser.add_option(
        '-t', '--max-thread', dest='maxthread', type='int', default=1000,
        help='MaxThread spawned to serve request, default is 1000')
    parser.add_option(
        '-v', '--verbose', dest='verbose', default=False,
        help='verbose logging')
    parser.add_option(
        '-d', '--work-dir', dest='workdir', default=None,
        help='working directory')
    parser.add_option(
        '-l', '--log-file', dest='logfile', default="httpserver.log",
        help='log file name')
    options, args = parser.parse_args()

    print 'Initialized stuff...'
    #httpwrapper.setup_logging(options.logfile, options.verbose, options.workdir)
    print 'Starting %s processes, listen on %s:%d ' % (options.number_of_processes, options.host, options.port)
    httpserver = httpwrapper.HTTPServer(options.host, options.port, options.number_of_processes, options.logfile, options.verbose, options.workdir)
    telegramBot = TelegramBot(TELEGRAM_TOKEN)
    msgSender  = MsgSender(telegramBot, queue)
    msgSender.start()
    httpserver.start()

if __name__ == '__main__':
    main()
