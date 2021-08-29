import os
import base64
import hashlib
import requests
import json

import unittest
import boto3

def recording_mode():
    return "RECORDING" in os.environ and os.environ.get("RECORDING").lower() == "true"

def recorder(func):
    def wrapper(self):
        if recording_mode():
            recording_param = "recording"
        else:
            recording_param = "playing"
        requests.post(f'https://httpproxy.control.io/start_{recording_param}/{func.__name__}')
        func(self)
        requests.post(f'https://httpproxy.control.io/stop_{recording_param}/{func.__name__}')


    return wrapper


def read_config():
    with open(f'{os.path.dirname(__file__)}/config.json') as json_file:
        data = json.load(json_file)
    result = {}
    for item in data:
        result[item["OutputKey"]] = item["OutputValue"]
    return result

class MyTestCase(unittest.TestCase):
    key_id = None

    @classmethod
    def setUpClass(cls):
        cls.config = read_config()

        if recording_mode():
            s3_client = boto3.client('s3')
            with open(f'{os.path.dirname(__file__)}/2021-08-18.tar.gz', 'rb') as f:
                print(s3_client.put_object(Bucket=cls.config["BucketName"], Key="our_soft/2021-08-18.tar.gz", Body=f))

            with open(f'{os.path.dirname(__file__)}/2021-08-18.tar.gz', 'rb') as f:
                #Read the whole file at once
                data = f.read()
                sha = hashlib.sha256()
                sha.update(data)
                shavalue = sha.digest()
            kms_client = boto3.client("kms")
            signature_bytes = kms_client.sign(
                KeyId=cls.config["KeyId"],
                Message=shavalue,
                MessageType="DIGEST",
                SigningAlgorithm='RSASSA_PSS_SHA_256'
            )['Signature']
            print("Signature Bytes", signature_bytes)
            signature = base64.b64encode(signature_bytes).decode('ascii')
            print(signature)
            dyn_client = boto3.client("dynamodb")
            dyn_client.put_item(
                TableName='top_sec_download_meta',
                Item={
                    'release': {
                        'S': '2021-08-18'
                    },
                    'signature': {
                        'S': signature
                    }
                })


    @recorder
    def test_something(self):
        print(f'ansible-playbook -vvv --connection=local --inventory 127.0.0.1, --limit 127.0.0.1 --extra-vars "key_id={self.config["KeyId"]} bucket={self.config["BucketName"]}" {os.path.dirname(__file__)}/../src/ansible.yml')
        os.system(f'ansible-playbook --connection=local --inventory 127.0.0.1, --limit 127.0.0.1 --extra-vars "key_id={self.config["KeyId"]} bucket={self.config["BucketName"]}" {os.path.dirname(__file__)}/../src/ansible.yml')
        self.assertEqual(os.path.isfile("/tmp/successful_check.txt") , True)

if __name__ == '__main__':
    unittest.main()
