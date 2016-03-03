from flask import Flask
from flask import request, make_response
import json
import logging
from logging.handlers import RotatingFileHandler
import httpwrapper
import Queue

app = Flask(__name__)
queue = Queue.Queue()
logger = logging.getLogger()

@app.route('/sendmsg', methods=['POST'])
def apiHandler():
  try:
    logger.info('receive request')
    chat_id = None
    if request.form.has_key('id'):
      chat_id = request.form['id']
    if request.form.has_key('msg'):
      text = request.form['msg']
    if text:
      queue.put([chat_id, text])
      data = {'id' : chat_id, 'msg' : text}
      resp = make_response(json.dumps(data))
      resp.headers.set('Server', httpwrapper.__version__)
      resp.headers.set('Content-Type', 'application/json')
      return resp
  except Exception, ex:
    print ex
