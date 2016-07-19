from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import count
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-k', dest='kmercount', type=int)
args = parser.parse_args()
k = args.kmercount 

def get_samples(filename):
    samples = []
    for sample in open(filename).readlines():
        samples.append(sample.strip()[:-4])
    return samples

samples = get_samples('/root/istc_oceanography/metadata/valid_samples_GA03_filenames.csv')
master_url = open("/root/spark-ec2/cluster-url").read().strip()
context = SparkContext(master_url)
context.setLogLevel("WARN")
sqlcontext = SQLContext(context)

def extract_kmers(r):
    for i in range(0,len(r.seq)-k+1):
        yield r.seq[i:i+k]

for sample_name in samples:
    sample_filename = "s3n://helgag/ocean_metagenome/overlapped/{sample_name}.csv".format(sample_name=sample_name)
    customSchema = StructType([ \
                StructField("id", StringType(), True), \
                StructField("seq", StringType(), True)])
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true').load(sample_filename, schema=customSchema).repartition(80)
    sample = sample.flatMap(extract_kmers).map(Row("kmer")).toDF().groupBy("kmer").agg(count("*"))
    #Toggle comment the following to export the data
    #sample.registerTempTable(sample_name + "_count")
    sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+'.csv')
    #Or this for pushing to s3
    #sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save('s3n://oceankmers/overlapped/'+sample_name+'.csv')

