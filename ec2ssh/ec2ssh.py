import boto3
import paramiko
#
# Name - ec2ssh.py
# Current version - v1.2
# Last modified on - 28-12-17
# Last modified by - Harleen Mann
#
# Created by - Harleen Mann
# Description - This script is called by cloudwatch on ec2 instance changing to "running" state
# Notes
    # v1.2: added code to start spark master process,spark slave process, spark thrift server, notebook server
#
#
# hosts below are hive-metastore-uat, spark-master-uat
#hosts = ['i-03047e9a091d6b01d', 'i-0d6e613cbca0466a4']

hosts_ip = { "i-03047e9a091d6b01d" : "10.29.5.184", "i-0d6e613cbca0466a4" : "10.29.5.91" }
hosts_username = { "i-03047e9a091d6b01d" : "ubuntu", "i-0d6e613cbca0466a4" : "ubuntu" }
hosts_source_key_locs = { "i-03047e9a091d6b01d" : "harleen/ssh/harleen-key-pair.pem", "i-0d6e613cbca0466a4" : "harleen/ssh/mod-it-harleen.pem"}
hosts_target_key_locs = { "i-03047e9a091d6b01d" : "/tmp/harleen-key-pair.pem", "i-0d6e613cbca0466a4" : "/tmp/mod-it-harleen.pem"}
hosts_bucket_locs = { "i-03047e9a091d6b01d" : "modharleen", "i-0d6e613cbca0466a4" : "modharleen" }
hosts_commands = { "i-03047e9a091d6b01d" : ["screen -md -S metastore",
                                    "screen -S metastore -X stuff $'\n/home/ubuntu/apache-hive-1.0.0-bin/bin/hive --service metastore\n'"
                                   ],
                   "i-0d6e613cbca0466a4" : ["screen -d -m /home/ubuntu/spark-2.2.1-bin-hadoop2.7/sbin/start-master.sh", 
                                   "screen -d -m /home/ubuntu/spark-2.2.1-bin-hadoop2.7/sbin/start-slaves.sh",
                                   "screen -d -m /home/ubuntu/spark-2.2.1-bin-hadoop2.7/sbin/start-thriftserver.sh",
                                   "screen -d -m -S notebook",
                                   "screen -S notebook -X stuff $'\nsource activate ec2ssh\njupyter notebook\n'"
                                  ]
                 }

def lambda_handler(event, context):
    hosts = [event['detail']['instance-id']]
    s3_client = boto3.client("s3") 
    for host in hosts:
        s3_client.download_file(hosts_bucket_locs[host],hosts_source_key_locs[host],hosts_target_key_locs[host])    
        k = paramiko.RSAKey.from_private_key_file(hosts_target_key_locs[host])
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to " + host)
        c.connect( hostname = hosts_ip[host], username = hosts_username[host], pkey = k )
        print("Connected to " + host)
        for command in hosts_commands[host]:
            print ("Executing {}".format(command))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
            print (stderr.read())
