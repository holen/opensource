import luigi
import random
from streams import Streams

class StreamsHdfs(Streams):
    def output(self):
        return luigi.contrib.hdfs.HdfsTarget(self.date.strftime('data/streams_%Y_%m_%d_faked.tsv'))
