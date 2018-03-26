import boto3
import os


aws_access_key_id = os.getenv("AWS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)


# Remove S3 Bucket
def remove_bucket(bucket_name):
    bucket = session.resource('s3').Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()


# Remove Route53
def remove_route53(name):
    client = session.client('route53')
    hosted_zone_id = os.getenv('HOSTED_ZONE_ID')
    alias_hosted_zone_id = os.getenv('ALIAS_HOSTED_ZONE_ID')

    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Creating QA subdomain for ' + name,
            'Changes': [
                {
                    'Action': 'DELETE',
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

# Remove the Stack
def init(name):
    site = name+".pburris.me"
    remove_bucket(site)
    remove_route53(site)
