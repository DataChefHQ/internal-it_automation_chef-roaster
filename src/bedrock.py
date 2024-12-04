from flask import jsonify
import boto3
import json
from botocore.exceptions import ClientError

REGION = "us-east-1"
MODEL_ID = "amazon.nova-pro-v1:0"


# Define the prompt for the model.
user_message = "Describe the purpose of a 'hello world' program in one line."

messages = [{"role": "user", "content": [{"text": user_message}]}]

bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)

response = bedrock_runtime.converse(
    modelId=MODEL_ID,
    messages=messages,
    inferenceConfig={"temperature": 0.7, "topP": 0.9, "maxTokens": 1024}
 )

response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)


def find_chef(request):
    return jsonify({"name": "Ali", "reason": "bluh bluh bluh ..."})
