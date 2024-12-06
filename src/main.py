import json
import os
from flask import Flask, render_template, jsonify, request
import boto3
import awsgi
from .bedrock import find_chef, generate_roast_image_url

app = Flask(__name__)
s3 = boto3.client('s3')
bucket = os.environ.get('BUCKET_NAME', "chef-roaster")


@app.after_request
def add_cache_control(response):
    # Disable caching for all responses
    response.cache_control.no_store = True
    response.expires = -1
    response.headers['Pragma'] = 'no-cache'
    return response


def sign_image(key):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=3600  # URL valid for 1 hour
    )
    return url


def list_images():
    response = s3.list_objects_v2(Bucket=bucket, Prefix='team/')
    images = []
    if 'Contents' in response:
        for item in response['Contents']:
            if '-kid' not in item['Key']:
                images.append(item['Key'])
    return images


def get_image(chef):
    all_images = list_images()
    real = None
    hat = None
    for image in all_images:
        if f'team/{chef.lower()}.' in image:
            real = image
        if f'team/{chef.lower()}-hat.' in image:
            hat = image
    return real, hat


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/bedrock', methods=['GET', 'POST'])
def bedrock():
    return jsonify(find_chef(request.get_json()))


@app.route('/image', methods=['POST'])
def roast_image():
    return jsonify(generate_roast_image_url(request.get_json()))


@app.route('/find', methods=['POST'])
def submit():
    result = find_chef(request.get_json())
    real_image, image_with_hat = get_image(result['name'])
    return jsonify({
        "url": sign_image(real_image),
        "hat": sign_image(image_with_hat),
        "reason": result['reason'].replace('"', '')
    })


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
