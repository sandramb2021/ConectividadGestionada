import json
import boto3
from base64 import b64decode

def get_aws_credentials(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get('aws_access_key_id'), config_data.get('aws_secret_access_key'), config_data.get('region_name')
    

def response_lambda():

    aws_access_key_id, aws_secret_access_key, region_name = get_aws_credentials()
    cloudwatch_logs = boto3.client('logs',aws_access_key_id, aws_secret_access_key, region_name)
    log_group_name = '/aws'

    response = cloudwatch_logs.describe_log_streams(
        logGroupNamePrefix='AW'
    )
    for each in response['logsGroups']:
        print(each)

response_lambda()