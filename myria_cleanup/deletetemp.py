import ConfigParser, os

deployment_file = open('/usr/local/myria/myriadeploy/deployment.cfg')

config = ConfigParser.ConfigParser()
config.readfp(deployment_file)

command = """
ssh {w} "sudo -u postgres psql {m} -c \"select 'drop table ' || '\\\"' || tablename|| '\\\";' from pg_tables where tablename like '%:temp:%'\" -t | sudo -u postgres psql {m}"
"""

for worker in config.options('workers'):
    w = config.get('workers',worker)
    worker_host = w.split(':')[0]
    db_name = w.split(':')[3]
    os.system(command.format(w=worker_host, m=db_name))
