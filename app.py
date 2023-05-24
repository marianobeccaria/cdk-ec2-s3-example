#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_s3_example.ec2_s3_example_stack import Ec2S3ExampleStack


app = cdk.App()
Ec2S3ExampleStack(app, "ec2-s3-example")

app.synth()
