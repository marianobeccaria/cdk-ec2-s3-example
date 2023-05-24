from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)


class Ec2S3ExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "Ec2S3ExampleQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "Ec2S3ExampleTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))
