#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
import run
import message

CHUNK_SIZE=15

class Streaming:
  def __init__(self):
    self.cur_job_id = 0

    pass

  def map_func(self, input_rdd):

    if input_rdd.count() == 0:
      return
    print "running job: [{job_id}]".format(job_id=self.cur_job_id)
    # filter line with tags

    #num_partitions = (input_rdd.count() + CHUNK_SIZE - 1) / CHUNK_SIZE

    result_message = run.streaming_based_main(
      input_stream=input_rdd.collect(),
      job_id=self.cur_job_id)

    mq = message.MqMessage()
    mq.send(result_message)
    mq.close()
    self.cur_job_id = self.cur_job_id + 1

def main():
  app_name = "Pubmed Word Mining"
  master = "spark://app08:7077"
  sconf = SparkConf().setAppName(app_name).setMaster(master)
  sc = SparkContext(conf=sconf)
  ssc = StreamingContext(sc, 1)

  # Create a DStream that will connect to hostname:port, like localhost:9999
  stm = Streaming()
  lines = ssc.textFileStream("/gcbi/storage/similarPubmed/input/")

  cleaned_lines = lines.filter(lambda line: len(line.split("\t")) == 3 )

  cleaned_lines.foreachRDD(lambda rdd: stm.map_func(rdd))
  #cleaned_lines.foreachRDD(lambda rdd: rdd.count()).pprint()

  # Split each line into words
  #words = lines.flatMap(lambda line: line.split(" "))

  ssc.start()             # Start the computation
  ssc.awaitTermination()  # Wait for the computation to terminate


if __name__ == "__main__":

  main()
