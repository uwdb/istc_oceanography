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
context = SparkContext(master_url)
context.setLogLevel("WARN")
sqlcontext = SQLContext(context)

def extract_kmers(r):
    if r.id[-1] == '2':
        seq = reverse_complement(r.seq)
        for i in range(len(seq)-k+1):
            yield seq[i:i+k]
    else:
        for i in range(0,len(r.seq)-k+1):
            yield r.seq[i:i+k]

def reverse_complement(s):
    complement= {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
    new_s = ''
    for i in range(len(s)):
        new_s += complement[s[len(s)-i-1]]
    return new_s

for sample_name in samples: 
    sample_filename = "s3n://helgag/ocean_metagenome/overlapped/{sample_name}.csv".format(sample_name=sample_name)
    customSchema = StructType([ \
                StructField("id", StringType(), True), \
                StructField("seq", StringType(), True)])
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true').load(sample_filename, schema=customSchema).repartition(80)
    sample = sample.flatMap(extract_kmers).map(Row("kmer")).toDF().groupBy("kmer").agg(count("*"))
    sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+str(k)+'.csv')
    
    # now for the non-overlapped version of the same dataset
    sample_filename = "s3n://helgag/ocean_metagenome/nonoverlapped/{sample_name}.csv".format(sample_name=sample_name)
    customSchema = StructType([ \
                StructField("id", StringType(), True), \
                StructField("seq", StringType(), True)])
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true').load(sample_filename, schema=customSchema).repartition(80)
    sample = sample.flatMap(extract_kmers).map(Row("kmer")).toDF().groupBy("kmer").agg(count("*")) 
    sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+str(k)+'NO.csv')
    #Pushing to s3
    #sample.repartition(1).write.format('com.databricks.spark.csv').options(header='true').save('s3n://oceankmers/overlapped/'+sample_name+'.csv')
