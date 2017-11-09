import boto3
import argparse
import json

'''
This script sets up the VPC Private Link(VPC Endpoint) for each AWS services currently supported.
'''

parser = argparse.ArgumentParser(
    description='VPC Endpoint Setup')
parser.add_argument(
    '--subnet-ids',
    action='store',
    dest='subnet_ids',
    required=True,
    nargs='*',
    help='Subnet IDs that you want to setup vpc endpoint. Basically you should specify at least 2 subnets located in different availability zone.'
)
parser.add_argument(
    '--security-group',
    action='store',
    dest='security_group',
    required=True,
    help='Security group for vpc endpoint'
)

args = parser.parse_args()
security_group = args.security_group

# makesure every subnets in same VPC.
ec2 = boto3.client('ec2')
subnet_ids = args.subnet_ids
vpc_id = map(lambda x : x['VpcId'],ec2.describe_subnets(SubnetIds=subnet_ids)['Subnets'] )
if not len(set(vpc_id)) == 1:
    print('all subnets have to be in same VPC.')
    quit(1)
else:
    vpc_id = vpc_id[0]

def filter_gateay_service(vpce_service):
    if vpce_service['ServiceType'][0]['ServiceType'] == 'Gateway':
        return False
    else:
        return True

# List available serivces for VPC endpoint(except S3 and DynamoDB as Gateway Type endpoint.).
response = ec2.describe_vpc_endpoint_services()
vpc_services = map(lambda x : x['ServiceName'], filter( filter_gateay_service, response['ServiceDetails']) )

# As vpc endpoint is located inside VPC by design, you don't have to care about the open IPs.
request = {
    'VpcId' : vpc_id,
    'VpcEndpointType' : 'Interface',
    'ServiceName' : '',
    'SecurityGroupIds' : [security_group],
    'SubnetIds' : subnet_ids
}

for vpc_service in vpc_services:
    request['ServiceName'] = vpc_service
    try:
        response = ec2.create_vpc_endpoint(**request)
    except Exception as e:
        print(e.message)
