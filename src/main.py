import json
import os
import time
from flask import Flask, render_template, jsonify, request
import boto3
import awsgi
from bedrock import find_chef

app = Flask(__name__)
s3 = boto3.client('s3')
bucket = os.environ.get('BUCKET_NAME', "chef-roaster")


def sign_image(key):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': f'team/{key}'},
        ExpiresIn=3600  # URL valid for 1 hour
    )
    return url


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/bedrock', methods=['GET', 'POST'])
def bedrock():
    return find_chef(request.get_json())


@app.route('/find', methods=['POST'])
def submit():
    time.sleep(5)
    return jsonify({"url": sign_image('ali.jpg')})


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    """Catches all requests."""
    return jsonify({'error': f'Path {path} is not allowed.'}), 404


def lambda_handler(event, context):
    if 'source' in event and event['source'] == 'serverless-plugin-warmup':
        return {}
    print(json.dumps(event))
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)
