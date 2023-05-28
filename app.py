#!/usr/bin/env python3

import aws_cdk as cdk
import configparser

from vpc_ec2_s3.vpc_ec2_s3_stack import VpcEc2S3Stack

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

VpcEc2S3Stack(app, "ec2-s3-example", env=env, MyInstance=ec2instance, VpcInfo=vpc_info)

app.synth()
