#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import pika
import config

class MqMessage():
    def __init__(self):
        user    = config.rabbitmq['user']
        passwd  = config.rabbitmq['passwd']
        host    = config.rabbitmq['host']

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

        print exchange
        print queueName

        self.channel.basic_publish(
            exchange=exchange, 
            routing_key=queueName,
            properties=pika.BasicProperties(
                content_type='text/plain',
                content_encoding='UTF-8'
            ),
            body=msg)

    def getQueue(self):
        return self.queue

    def setConsume(self, queueName=None):
        def callback(ch, method, properties, body):
            print(" [x] [{prop}]\tReceived: {body}".format(prop=properties,
                                                           body=body))
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
