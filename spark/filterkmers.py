from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import count,udf
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('-k', dest='kmercount', type=int)
#parser.add_argument('-o', dest='overlapped', type=int, help='1 for overlapped, 0 for non-overlapped')
args = parser.parse_args()
k = args.kmercount 
#overlapped = args.overlapped

def get_samples(filename):
    samples = []
    for sample in open(filename).readlines():
        samples.append(sample.strip()[:-4])
    return samples

samples = get_samples('/root/istc_oceanography/metadata/valid_samples_GA02_filenames.csv')
samples += get_samples('/root/istc_oceanography/metadata/valid_samples_GA03_filenames.csv')
master_url = open("/root/spark-ec2/cluster-url").read().strip()
masterHostname = open("/root/spark-ec2/masters").read().strip()
context = SparkContext(master_url)
context.setLogLevel("WARN")
sqlcontext = SQLContext(context)

for sample_name in samples[:28]: 
    sample_filename = "hdfs://{masterhostname}:9000/user/root/{sample_name}.csv/part-00000".format(masterhostname=masterHostname, sample_name=sample_name)
    customSchema = StructType([ \
                StructField("kmer", StringType(), True), \
                StructField("cnt", StringType(), True)])
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true').load(sample_filename, schema=customSchema).repartition(80)
    sample = sample.filter("kmer not like '%N%'" )
    sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+'_filtered_'+str(k)+'.csv')
    
    sample_filename = "hdfs://{masterhostname}:9000/user/root/{sample_name}NO.csv/part-00000".format(masterhostname=masterHostname, sample_name=sample_name)
    customSchema = StructType([ \
                StructField("kmer", StringType(), True), \
                StructField("cnt", StringType(), True)])
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true').load(sample_filename, schema=customSchema).repartition(80)
    sample = sample.filter("kmer not like '%N%'" )
    sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+'_filteredNO_'+str(k)+'.csv')
    
