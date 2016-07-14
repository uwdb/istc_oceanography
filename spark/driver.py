from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row

k = 11 # Length of k-mers
samples = ['S0001_n1000', 'S0002_n1000']
master_hostname = open("/root/spark-ec2/masters").read().strip()
master_url = open("/root/spark-ec2/cluster-url").read().strip()
context = SparkContext(master_url)
context.setLogLevel("WARN")
sqlcontext = SQLContext(context)

def extract_kmers(r):
    for i in range(0,len(r.seq)-k+1):
        yield r.seq[i:i+k]

for sample_name in samples:
    sample_filename = "hdfs://{hostname}:9000/data/{sample_name}.csv".format(hostname=master_hostname, sample_name=sample_name)
    sample = sqlcontext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(sample_filename)
    sqlcontext.registerDataFrameAsTable(sample, sample_name)
    kmers = sample.flatMap(extract_kmers).collect()
    kmer_rows = map(lambda x: Row(SampleID=sample_name, kmer=x),kmers)
    kmers_df = sqlcontext.createDataFrame(kmer_rows)
    kmers_df.registerTempTable("kmers"+sample_name)
    sqlcontext.sql("select SampleID, kmer, count(*) as count from kmers{sample_name} group by SampleID, kmer order by count desc".format(sample_name=sample_name)).registerTempTable(sample_name + '_count')

X_sql = """
select a.SampleID as asample, b.SampleID as bsample,
       case when a.count < b.count then a.count else b.count end as minv,
       a.count as acount, b.count as bcount
       from {sample1} a, {sample2} b
       where a.kmer = b.kmer
""".format(sample1=samples[0]+'_count', sample2=samples[1]+'_count')
sqlcontext.sql(X_sql).registerTempTable('X')

sum_sql = """
select sum(acount) + sum(bcount) as sum_samp from X
"""
sqlcontext.sql(sum_sql).registerTempTable('sumX')

Y_sql = """
select asample, bsample, 1 - 2*sum(minv) / sum_samp from X, sumX
group by asample, bsample, sum_samp
"""
sqlcontext.sql(Y_sql).show()
