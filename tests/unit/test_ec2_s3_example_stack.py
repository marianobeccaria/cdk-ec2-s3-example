import aws_cdk as core
import aws_cdk.assertions as assertions
from ec2_s3_example.ec2_s3_example_stack import Ec2S3ExampleStack


def test_sqs_queue_created():
    app = core.App()
    stack = Ec2S3ExampleStack(app, "ec2-s3-example")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = Ec2S3ExampleStack(app, "ec2-s3-example")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
