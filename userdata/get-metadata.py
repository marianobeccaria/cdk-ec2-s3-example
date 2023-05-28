#!/usr/bin/python3

import requests

def get_instance_data():
    instance_identity_url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
    session = requests.Session()
    r = requests.get(instance_identity_url)
    response = r.json()

    file = open("/tmp/ec2-instance.info", "w")
    
    file.write("[EC2 Instance Info]\n")
    for key,val in response.items():
        line = f'{key}={val}\n'
        file.write(line)

    file.close()

get_instance_data()
