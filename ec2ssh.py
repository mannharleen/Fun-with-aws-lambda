import boto3
import paramiko

hosts = ['10.29.5.184']
commands = [        "ls",        "echo $JAVA_HOME"        ]

def ssh_ex_commands(event, context):
    s3_client = boto3.client("s3") 
    s3_client.download_file("modharleen","harleen/ssh/harleen-key-pair.pem","/tmp/harleen-key-pair.pem")    
    k = paramiko.RSAKey.from_private_key_file("/tmp/harleen-key-pair.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hosts:
        print("Connecting to " + host)
        c.connect( hostname = host, username = "ubuntu", pkey = k )
        print("Connected to " + host)
    for command in commands:
        print ("Executing {}".format(command))
        stdin , stdout, stderr = c.exec_command(command)
        print (stdout.read())
        print (stderr.read())
