import json
from flask import Flask, render_template, jsonify, request
import boto3
import awsgi
from bedrock import find_chef

app = Flask(__name__)
s3_client = boto3.client('s3')



@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/bedrock', methods=['GET', 'POST'])
def bedrock():
    return find_chef(request.get_json())


@app.route('/submit', methods=['POST'])
def submit():
    # Return a loading message while processing in the background
    return jsonify({"status": "loading", "message": "Processing your request..."})


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
