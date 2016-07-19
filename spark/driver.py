from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import count

def get_samples(filename):
    samples = []
    for sample in open(filename).readlines():
        samples.append(sample.strip()[:-4])
    return samples

k = 11 # Length of k-mers
samples = get_samples('/root/istc_oceanography/metadata/valid_samples_GA02_filenames.csv')
master_hostname = open("/root/spark-ec2/masters").read().strip()
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
    #sample.flatMap(extract_kmers).map(Row("kmer")).toDF().groupBy("kmer","SampleID").agg(count("*")).repartition(1).write.format('com.databricks.spark.csv').options(header='true').save('s3n://oceankmers/overlapped/'+sample_name+'.csv')
    sample.flatMap(extract_kmers).map(Row("kmer")).toDF().groupBy("kmer").agg(count("*")).repartition(1).write.format('com.databricks.spark.csv').options(header='true').save(sample_name+'.csv')
    #kmers_df.registerTempTable("kmers"+sample_name)
    #sqlcontext.sql("select kmer, count(*) as count from kmers{sample_name} group by kmer".format(sample_name=sample_name)).repartition(1).write.format('com.databricks.spark.csv').options(header='true').save('s3n://oceankmers/overlapped/'+sample_name+'.csv')
    #sqlcontext.sql("select kmer, count(*) as count from kmers{sample_name} group by kmer".format(sample_name=sample_name)).registerTempTable(sample_name + '_count')
    #Uncomment the following to export
    #sqlcontext.sql("select * from {s}".format(s=sample_name + '_count')).repartition(1).write.format('com.databricks.spark.csv').options(header='true').save('s3n://oceankmers/overlapped/'+sample_name+'.csv')

#X_sql = """
#select a.SampleID as asample, b.SampleID as bsample,
#       case when a.count < b.count then a.count else b.count end as minv,
#       a.count as acount, b.count as bcount
#       from {sample1} a, {sample2} b
#       where a.kmer = b.kmer
#""".format(sample1=samples[0]+'_count', sample2=samples[1]+'_count')
#sqlcontext.sql(X_sql).registerTempTable('X')

#suma_sql = """
#select sum(a.count) as sum_a from {s1} a
#""".format(s1=samples[0]+'_count') 
#sqlcontext.sql(suma_sql).registerTempTable('sumA')

#sumb_sql = """
#select sum(b.count) as sum_b from {s2} b
#""".format(s2=samples[1]+'_count') 
#sqlcontext.sql(sumb_sql).registerTempTable('sumB')

#Y_sql = """
#select asample, bsample, 1 - 2*sum(minv) / (sum_a+sum_b) from X, sumA, sumB
#group by asample, bsample, sum_a, sum_b
#"""
#sqlcontext.sql(Y_sql).show()
