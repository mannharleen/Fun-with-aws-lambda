import boto3
#
# Name - startEC2Instance.py
# Current version - v1.2
# Last modified on - 28-12-17
# Last modified by - Harleen Mann
#
# Created by - Harleen Mann
# Description - This script is called by cloudwatch trigger based on the schedule time
# Notes
    # v1.2: Added qlik-uat-env and talend-uat-env servers
#
#
region = 'ap-southeast-1'
instances = ['i-01d57c6e17451c2ef', 'i-0befd69a2f0c86cd3', 'i-0c9297af766518a54'] 
# instance added in same order = centOS-harleen, qlikUAT, talendUAT

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print ('starting your instances: ' + str(instances))

