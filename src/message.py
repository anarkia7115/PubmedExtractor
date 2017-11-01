#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import pika
import sys
import config

CHUNK_SIZE=6

class MqMessage():
  def __init__(self):
    user  = config.rabbitmq['user']
    passwd  = config.rabbitmq['passwd']
    host  = config.rabbitmq['host']

    cred = pika.PlainCredentials(user, passwd)
    params = pika.ConnectionParameters(host, credentials=cred)
    self.connection = pika.BlockingConnection(params)

    self.channel = self.connection.channel()

  def getChannel(self):
    return self.channel

  def close(self):
    self.connection.close()

  def getConnection(self):
    return self.connection

  def send(self, msg, exchange=None, queueName=None):
    if exchange is None:
      exchange = config.rabbitmq['exchange_name']

    if queueName is None:
      queueName = config.rabbitmq['queue_name_callback']

    print "exchange: {}".format(exchange)
    print "queueName: {}".format(queueName)
    print "message: {}".format(msg)

    try:
      self.channel.basic_publish(
        exchange=exchange, 
        routing_key=queueName,
        properties=pika.BasicProperties(
          content_type='text/plain',
          content_encoding='UTF-8'
        ),
        body=msg)
    except pika.exceptions.ConnectionClosed():
      print("msg send failed")
    except:
      print("Unexpected error:", sys.exc_info()[0])
      raise

  def getQueue(self):
    return self.queue

  def setConsume(self, queueName=None):
    def callback(ch, method, properties, body):
      # body print to log
      logBody = (body[:75] + '..') if len(body) > 75 else body
      print(" [x] [{prop}]\tReceived: {body}".format(prop=properties,
                               body=logBody))

      # chunk message to small pieces if big enough
      import render
      msgBody = render.Body(body, CHUNK_SIZE)
      msgBody.genPmidList()

      # big message
      if msgBody.getPmidSize() >= CHUNK_SIZE:
        for chunkMsg in msgBody.chunkPmids():
          self.queue.put(chunkMsg)
      # small message
      else:
        self.queue.put(body)

      print "Queue Size: {}".format(self.queue.qsize())

    if queueName == None:
      queueName = config.rabbitmq['queue_name']
    self.channel.basic_consume(
      callback, 
      queue=queueName,
      no_ack=True)

  def start_consuming(self, queue=None):
    if queue is None:
      print "---mq.queue set as new queue---"
      import multiprocessing
      self.queue = multiprocessing.Queue()
    else:
      print "---mq.queue set as waiter.queue---"
      self.queue = queue

    self.channel.start_consuming()

def main():
  exchange = config.rabbitmq['exchange_name']
  queueName = config.rabbitmq['queue_name']

  mqm = MqMessage()

  jsonString = "[1,2,3,4,5,6,7,8,9,0]"
  mqm.send(jsonString, exchange, queueName)

if __name__ == "__main__":
  main()

