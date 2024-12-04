from flask import jsonify
import boto3
import random
from botocore.exceptions import ClientError

def read_txt_file(filename: str) -> str:
    with open(filename, 'r') as file:
        content = file.read()
    return content

REGION = "us-east-1"
MODEL_ID = "amazon.nova-pro-v1:0"
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_LEN = 1024
MAX_INPUT_LEN = 5000
CHEFS = ["Ali", "Andrea", "Anne", "Ashkan", "Bram", "Davide", "Farbod", "Federico", "Jane", "Kiarash", "Mahdokht", "Melvyn", "Pejman", "Rehan", "Shahin", "Soheil"]
DESCRIPTIONS = read_txt_file("src/prompts/descriptions.txt")

def guess_the_chef_name(user_message: str, descriptions: str) -> str:
    """
    Get a response from the Bedrock AI model.
    """
    prompt = f"Persons Descriptions: \n{descriptions}\nUser input: {user_message}\nBased on the User input and the descriptions of the persons above, guess who is the input is about? NO MATTER WHAT ONLY output their name without anything before or after it."
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)
    
    try:
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={"temperature": TEMPERATURE, "topP": TOP_P, "maxTokens": MAX_LEN}
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except ClientError as e:
        return f"Error communicating with Bedrock: {str(e)}"

def get_the_roast(user_message: str, chef_to_roast: str, descriptions: str) -> str:
    """
    Get a response from the Bedrock AI model.
    """
    prompt = f"DataChef Roasting Party! \n\nHere’s the next person: {chef_to_roast}. Some information about them:\n{descriptions}\n\nDish out the funniest, most hilarious roast for {chef_to_roast}. Keep it short, FUNNY, and spicy. It doesn't need to be necessarily from their information. ONLY GIVE ME THE ROAST — nothing else!"
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)
    
    try:
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={"temperature": TEMPERATURE, "topP": TOP_P, "maxTokens": MAX_LEN}
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except ClientError as e:
        return f"Error communicating with Bedrock: {str(e)}"

def check_and_handle_miss_guessed_chef(guessed_chef, chefs=CHEFS):
    lower_chefs = [i.lower() for i in chefs]
    if guessed_chef.lower() in lower_chefs:
        return guessed_chef.lower()
    else:
        print("Guess Randomly")
        return random.choice(chefs).lower()

def find_chef(request):
    print(request) 
    print("###")
    try:
        user_message = request['prompt']
    except KeyError:
        user_message = request['message']
    if len(user_message) >= MAX_INPUT_LEN:
        user_message = request['prompt'][:MAX_INPUT_LEN]
    if user_message == "":
        user_message = "No Description Available!"

    guessed_chef = guess_the_chef_name(user_message=user_message, descriptions=DESCRIPTIONS)
    print(f"## {guessed_chef}")
    guessed_chef = check_and_handle_miss_guessed_chef(guessed_chef)
    print(f"### {guessed_chef}")
    roast = get_the_roast(user_message=user_message, chef_to_roast=guessed_chef, descriptions=DESCRIPTIONS)
    print(f"$$$ {roast}")
    return {"name": guessed_chef, "reason": roast}
