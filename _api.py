from __future__ import unicode_literals
import telegram
import gevent.monkey
from datetime import datetime
import threading
import time
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_all()

# ambient Bot telegram api token
TELEGRAM_TOKEN = '190093517:AAHNUmk_ockALEMU-Ud_oUA2Lb5sReAj8rM'

class AmbientBot(object):
  def __init__(self):
    self.connection = telegram.Bot(token = TELEGRAM_TOKEN)
    conversationMessages = self.connection.getUpdates()
    self.chatIdList = []
    for msg in conversationMessages:
      if msg.message.chat_id not in self.chatIdList:
        self.chatIdList.append(msg.message.chat_id)
    self.concurrentMsg = 0
    self.CURRENT_MINUTE = -1

  def sendMsg(self, id, message):
    if not id:
      for id in self.chatIdList:
        self.connection.sendMessage(id, message)
    else:
      self.connection.sendMessage(chat_id = id, text = message)


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
        item = self.queue.get()
        print item
        self.bot.sendMsg(item[0], item[1])
      time.sleep(4)







