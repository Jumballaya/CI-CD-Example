import boto3
import os


aws_access_key_id = os.getenv("AWS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)


# Make S3 Bucket
def make_bucket(bucket_name):
    client = session.client('s3')

    bucket_policy = '{"Version": "2008-10-17","Statement": [{"Effect": "Allow","Principal": "*","Action": "s3:GetObject","Resource": "arn:aws:s3:::'+bucket_name+'/*"}]}'

    client.create_bucket(
        ACL="public-read",
        Bucket=bucket_name,
    )

    client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=bucket_policy
    )

    client.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {
                'Suffix': 'index.html',
            },
        }
    )

# Make Route53
def make_route53(name):
    client = session.client('route53')
    hosted_zone_id = os.getenv('HOSTED_ZONE_ID')
    alias_hosted_zone_id = os.getenv('ALIAS_HOSTED_ZONE_ID')

    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Creating QA subdomain for ' + name,
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': alias_hosted_zone_id,
                            'DNSName': 's3-website-us-east-1.amazonaws.com',
                            'EvaluateTargetHealth': True,
                        },
                    },
                }
            ],
        }
    )

# Make Codebuild
def make_codebuild(name, commit):
    client = session.client('codebuild')

    client.start_build(
        projectName='pburris-me_Stage',
        sourceVersion=commit,
        environmentVariablesOverride=[
            {
                'name': 'BUCKET_NAME',
                'value': name,
                'type': 'PLAINTEXT',
            }
        ],
    )


# Build the stack
def init(name, commit):
    site = name+".pburris.me"
    make_bucket(site)
    print("Making Bucket")
    make_route53(site)
    print("Setting DNS")
    make_codebuild(name, commit)
    print("Done Building")

