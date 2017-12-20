import boto3
import paramiko

hosts = ['10.29.5.184']
commands = { "10.29.5.184" : ["screen -md /home/ubuntu/apache-hive-1.0.0-bin/bin/hive --service metastore", "ls" ] }
source_key_locs = { "10.29.5.184" : "harleen/ssh/harleen-key-pair.pem" }
target_key_locs = { "10.29.5.184" : "/tmp/harleen-key-pair.pem" }
bucket_locs = { "10.29.5.184" : "modharleen" }

def ssh_ex_commands(event, context):
    s3_client = boto3.client("s3") 
    for host in hosts:
        s3_client.download_file(bucket_locs[host],source_key_locs[host],target_key_locs[host])    
        k = paramiko.RSAKey.from_private_key_file(target_key_locs[host])
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to " + host)
        c.connect( hostname = host, username = "ubuntu", pkey = k )
        print("Connected to " + host)
        for command in commands[host]:
            print ("Executing {}".format(command))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
            print (stderr.read())
