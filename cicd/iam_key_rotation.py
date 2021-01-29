import boto3
import requests
import os

iam_client = boto3.client('iam')
secrets_manager_client = boto3.client('secretsmanager')

def handler(event, context):
    iam_username = os.environ['DeployerUserName']
    cicd_platform_access_token_secret_key_arn = os.environ['CicdPlatformTokenSecretKeyArn']
    cicd_platform_rest_api = os.environ['CicdPlatformRestAPI']
    # An IAM user can have no more than 2 access keys at a time. so if it already has two, delete one of them before creating the new key
    keys = iam_client.list_access_keys(UserName=iam_username)['AccessKeyMetadata']

    if len(keys) == 2:
        k1 = keys[0]
        k2 = keys[1]
        if k2['Status'] == 'Active':
            key_to_delete = k1
        else:
            key_to_delete = k2
        iam_client.delete_access_key(UserName=iam_username, AccessKeyId=key_to_delete['AccessKeyId'])
        keys.remove(key_to_delete)

    new_key = iam_client.create_access_key(UserName=iam_username)
    # Now that the new access key got successfully created, delete the old one
    for key in keys:
        iam_client.delete_access_key(UserName=iam_username, AccessKeyId=key['AccessKeyId'])

    gitlab_access_token = secrets_manager_client.get_secret_value(SecretId=cicd_platform_access_token_secret_key_arn)['SecretString']
    headers = {"PRIVATE-TOKEN": gitlab_access_token}
    requests.put(cicd_platform_rest_api + "variables/AWS_ACCESS_KEY_ID", headers=headers,
                     data={"value": new_key['AccessKey']['AccessKeyId']})
    requests.put(cicd_platform_rest_api + "variables/AWS_SECRET_ACCESS_KEY", headers=headers,
                     data={"value": new_key['AccessKey']['SecretAccessKey']})
