from flask import Flask, render_template, jsonify
import boto3
import awsgi

app = Flask(__name__)
s3_client = boto3.client('s3')



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():

    # Return a loading message while processing in the background
    return jsonify({"status": "loading", "message": "Processing your request..."})


def lambda_handler(event, context):
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)