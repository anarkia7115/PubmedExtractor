#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

MAX_JOB_NUM=9999
REFRESH_INTERVAL=10

import time

class Waiter():
    def __init__(self):
        self.curJobId = 0

        import message
        self.mq = message.MqMessage()
        self.mq.setConsume()
        pass

    def start_consuming(self, queue):

        self.mq.start_consuming(queue)

    def get(self):
        inputList = self.queue
        inputString = inputList.get()
        return inputString

    def getWaitSize(self):
        inputList = self.queue
        return inputList.qsize()

    def run(self):

        import multiprocessing

        self.queue = multiprocessing.Queue()
        receiverThread = multiprocessing.Process(target=self.start_consuming,
                                                 kwargs={'queue':self.queue})
        receiverThread.start()
        print "out: is listener alive?  {is_alive}".format(
            is_alive=receiverThread.is_alive())

        while(self.curJobId < MAX_JOB_NUM):
            # check queue size
            jobSize = self.getWaitSize()
            print "job size: {job_size}".format(job_size=jobSize)

            # run job
            if jobSize > 0:
                print "running job: [{job_id}]".format(job_id=self.curJobId)
                inputString = self.get()
                import run
                resultMessage = run.main(inputString=inputString)
                self.mq.send(resultMessage)
                print "message sent: {}".format(resultMessage)
                self.curJobId += 1

            # check queue listener alive
            print "is listener alive?  {is_alive}".format(
                is_alive=receiverThread.is_alive())

            # sleep
            time.sleep(REFRESH_INTERVAL)

def main():
    waiter = Waiter()
    waiter.run()

if __name__ == "__main__":
    main()
