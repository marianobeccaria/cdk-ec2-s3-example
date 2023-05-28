# VPC, EC2 instance and S3 bucket example
## Description
This repo creates a VPC, an ec2 instance, and a bucket that's accessible from the instance with a role and read policy

## How to run this contract and deploy resources to AWS?
This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.

1. Install and configure `awscli` command tool in your local host.
   See: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

2. Install and configure `cdk` command line in your local host.
```
$ npm install -g aws-cdk
```

3. Clone this repository in your local host: 
```
$ git clone https://github.com/marianobeccaria/cdk-ec2-s3-example.git
```

4. Activate your python virtualenv:
   If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
   manually once the init process completes.
   To manually create a virtualenv on MacOS and Linux: `$ python3 -m venv .venv`

   Then activate the environment: 
    `source .venv/bin/activate`     (For Linux or Mac)

    `.venv\Scripts\activate.bat`     (For Windows)

Finally install requirements:  `pip install -r requirements.txt`

5. Rename file `config.ini-rename` to `config.ini` and edit it with your own info: AWS account ID, vpc ID, bucket, etc

6. Run `cdk synth` to verify there are no errors and to see the synthesized CloudFormation template for this code

7. Then run `cdk deploy` to deploy this stack to your default AWS account/region. 

8. In the AWS console verify that your CloudFormation stack is completed

## Other useful `cdk` commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## How to configure python environments in CDK Python project? 

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`ec2_s3_example_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.


After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.


Enjoy!
