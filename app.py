#!/usr/bin/env python3

import aws_cdk as cdk
import configparser

from ec2_s3_example.ec2_s3_example_stack import Ec2S3ExampleStack

config = configparser.ConfigParser()
config.read('./config.ini')
print("AWS Account: ", config.get('Settings','aws_account_id'))
print("Region: ", config.get('Settings','region'))
print("AMI: ", config.get('Instance','ami_image'))

app = cdk.App()

env = cdk.Environment(
  region=config.get('Settings','region'),
  account=config.get('Settings', 'aws_account_id')
)

vpc_info = config["VPC"]
ec2instance = config["Instance"]

Ec2S3ExampleStack(app, "ec2-s3-example", env=env, ec2instance=ec2instance, vpc_info=vpc_info)

app.synth()
