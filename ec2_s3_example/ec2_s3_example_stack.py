from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_s3 as s3,
)

import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

class Ec2S3ExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # AMI image: ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230516
        print("AMI Image: ", config.get('Settings','ami_image'))
        print("VPC ID: ",config.get('Settings', 'vpc_id'))

        self.instance_ami = config.get('Settings','ami_image')
        self.instance_type = config.get('Settings','ec2_type')
        self.vpc_id = config.get('Settings', 'vpc_id')
        #self.security_group_id = 
        self.key_name = "my-useast1-key-0001"
        self.key_type = "rsa"

        key_pair = ec2.CfnKeyPair(self, "MyEc2KeyPair", 
            key_name=self.key_name, 
            key_type=self.key_type
        )

        vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id=self.vpc_id)

        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc, allow_all_outbound=True)

        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4('172.31.0.0/16'),
            description="Allow SSH connection",
            connection=ec2.Port.tcp(22)
        )

        ec2_instance = ec2.Instance(self, "MyEc2Instance",
            instance_name="my-ec2-test01",
            instance_type=ec2.InstanceType(self.instance_type),
            machine_image=ec2.MachineImage().lookup(name=self.instance_ami),
            vpc=vpc,
            security_group=security_group,
            key_name=key_pair.key_name
        )
