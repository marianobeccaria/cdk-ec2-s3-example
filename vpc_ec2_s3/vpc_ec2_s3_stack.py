from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets,
    CfnOutput,
    Tags
)

import os

class VpcEc2S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, MyInstance=None, VpcInfo=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        region = os.environ["CDK_DEFAULT_REGION"]
        print(region)

        # Create a new keypair for the EC2 instance. 
        # To download key into a .pem see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html#create-key-pair-cloudformation
        # aws ssm get-parameter --name /ec2/keypair/key-05abb699beEXAMPLE --with-decryption --query Parameter.Value --output text > new-key-pair.pem
        key_pair = ec2.CfnKeyPair(self, "MyEc2KeyPair", 
            key_name = MyInstance["key_name"],
            key_type = MyInstance["key_type"]
        )

        # This will create a new VPC where they ec2 instance lives. However you can also use an existing VPC using the line below:
        # e.g:
        #   vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id=VpcInfo["vpc_id"])
        vpc = ec2.Vpc(self, "TheVPC",
            ip_addresses=ec2.IpAddresses.cidr(VpcInfo["vpc_ipaddress_cidr"]),
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

        # Creates a new Security group
        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc, allow_all_outbound=True)
        # Sets inbound rule to allow ssh traffic coming only from VPC 
        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(VpcInfo["vpc_ipaddress_cidr"]),
            description="Allow SSH connection from within VPC",
            connection=ec2.Port.tcp(22)
        )

        # Creates the EC2 Instance
        ec2_instance = ec2.Instance(self, "MyEc2Instance",
            instance_name="my-ec2-test01",
            instance_type=ec2.InstanceType(MyInstance["ec2_type"]),
            machine_image=ec2.MachineImage().lookup(name=MyInstance["ami_image"]),
            vpc=vpc,
            # Sets the ec2 instance IP address in the the private subnet
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            #vpc_subnets=ec2.SubnetSelection(name="Applications")
            security_group=security_group,
            key_name=key_pair.key_name,
            # Creates EBS devices. See size definition in config.ini file
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(int(MyInstance["ebs_root_size"]))
                ), 
                # Creates a second EBS volume with 5 GiB
                ec2.BlockDevice(
                    device_name="/dev/sdc",
                    volume=ec2.BlockDeviceVolume.ebs(5)
                )
            ],
        )

        # Created the bucket
        bucket = s3.Bucket(self, "MyBucket",
            bucket_name=MyInstance["bucket_01"],
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
        )

        # Add policy statement to default instance role
        ec2_instance.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:GetBucket*",
                "s3:GetObject*",
                "s3:List*"
            ],
            resources=[
                f'arn:aws:s3:::{bucket.bucket_name}',
                f'arn:aws:s3:::{bucket.bucket_name}/*',
            ]
        ))

        ####### USER DATA ########
        ec2_instance.user_data.add_commands("sudo apt update -y && sudo apt install python3-pip -y && sudo apt install awscli -y")

        # Add assest to instance user data
        file_name = "write_to_100.py"
        file_asset = aws_s3_assets.Asset(self, "UserDataAsset", path=f'./userdata/{file_name}')

        local_path = ec2_instance.user_data.add_s3_download_command(
            bucket=file_asset.bucket,
            bucket_key=file_asset.s3_object_key,
            local_file=f'/tmp/{file_name}',
            region="us-east-1"
        )

        ec2_instance.user_data.add_commands(f'chmod +x /tmp/{file_name}; /tmp/{file_name}\n')

        file_asset.grant_read(ec2_instance.role)

        ####### TAGS ##########
        Tags.of(bucket).add("Environment", "Dev") # Add tags for S3 bucket
        Tags.of(ec2_instance).add("Environment", "Dev") # Add tags for EC2 instance

        ####### OUTPUTS #######
        CfnOutput(self, "MyInstanceName", value=ec2_instance.instance_id)
        CfnOutput(self, "MyInstancePrivateIp", value=ec2_instance.instance_private_ip)
        CfnOutput(self, "MyBucketNAme", value=bucket.bucket_arn)