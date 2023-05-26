from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_s3 as s3,
)

class VpcEc2S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ec2instance=None, vpc_info=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key_pair = ec2.CfnKeyPair(self, "MyEc2KeyPair", 
            key_name = ec2instance["key_name"], 
            key_type = ec2instance["key_type"]
        )

        #vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id=vpc_info["vpc_id"])
        vpc = ec2.Vpc(self, "TheVPC",
            ip_addresses=ec2.IpAddresses.cidr(vpc_info["vpc_ipaddress_cidr"]),
            max_azs=1,

            subnet_configuration=[ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name="PublicIngress",
                cidr_mask=24
            ), ec2.SubnetConfiguration(
                cidr_mask=24,
                name="Applications",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ), ec2.SubnetConfiguration(
                cidr_mask=28,
                name="Databases",
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                reserved=True
            )
            ]
        )

        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc, allow_all_outbound=True)

        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_info["vpc_ipaddress_cidr"]),
            description="Allow SSH connection from within VPC",
            connection=ec2.Port.tcp(22)
        )

        ec2_instance = ec2.Instance(self, "MyEc2Instance",
            instance_name="my-ec2-test01",
            instance_type=ec2.InstanceType(ec2instance["ec2_type"]),
            machine_image=ec2.MachineImage().lookup(name=ec2instance["ami_image"]),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            #vpc_subnets=ec2.SubnetSelection(name="Applications")
            security_group=security_group,
            key_name=key_pair.key_name,
            # Creates EBS devices. See size definition in config.ini file
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(int(ec2instance["ebs_root_size"]))
                ), 
                # Creates and mounts a 5GiB volume
                ec2.BlockDevice(
                    device_name="/dev/sdc",
                    volume=ec2.BlockDeviceVolume.ebs(5)
                )
            ]
        )
