from __future__ import unicode_literals
import telegram
from datetime import datetime
import threading
import time
import sys
import logging

logger = logging.getLogger()

class TelegramBot(object):
  def __init__(self, _token):
    try:
      self.connection = telegram.Bot(token = _token)
      botInformation = self.connection.getMe()
      logger.info('Hello, my name is %s' %botInformation['first_name'])
    except Exception, ex:
      logger.error(ex)
      sys.exit(2)
    self.chatIdList = []
    conversationMessages = self.connection.getUpdates()
    for msg in conversationMessages:
      if msg.message.chat_id not in self.chatIdList:
        self.chatIdList.append(msg.message.chat_id)

  def sendMsg(self, id, message):
    logger.info('sending msg: %s' % message)
    try:
      if not id:
        for id in self.chatIdList:
          logger.info('to id %s' %id)
          self.connection.sendMessage(id, message)
      else:
        self.connection.sendMessage(chat_id = id, text = message)
    except Exception, ex:
      logger.error('got exception when sending message: %s', ex)

class MsgSender(threading.Thread):
  def __init__(self, telegramBot, queue):
    self.bot = telegramBot
    self.queue = queue
    threading.Thread.__init__(self)

  def run(self):
    '''
    item is a list with id and msg content [ 1343, 'alert msg' ]
    telegram api allows us to send < 20 msg / min

    '''
    while True:
      if not self.queue.empty():
        logger.info('polling for message....')
        item = self.queue.get()
        logger.info('got message with id: %s , content: %s' % (item[0], item[1]))
        self.bot.sendMsg(item[0], item[1])
      time.sleep(4)







