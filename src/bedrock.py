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
CHEFS = ["Ali", "Andrea", "Anne", "Ashkan", "Bram", "Davide", "Farbod", "Federico", "Jane", "Kiarash", "Mahdokht", "Melvyn", "Pejman", "Rehan", "Shahin", "Soheil"]
DESCRIPTION = """- Ali: Male, 24, Data Scientist, Iran - Tehran. 
- Andrea: Female, 29, Data Engineer, Italy - Milan. 
- Anne: Female, 32, Administrative Assistant, USA - New York. 
- Ashkan: Male, 35, Founder & CEO, Iran - Tehran. 
- Bram: Male, 28, Project Manager, Netherlands - Amsterdam. 
- Davide: Male, 27, Software Engineer, Italy - Rome. 
- Farbod: Male, 30, Software Engineer, Iran - Tehran. 
- Federico: Male, 33, Software (Data) Engineer, Italy - Bologna. 
- Jane: Female, 40, Executive Assistant, UK - London. 
- Kiarash: Male, 26, Machine Learning Engineer, Iran - Tehran. 
- Mahdokht: Female, 31, Data Scientist, Iran - Tehran. 
- Melvyn: Male, 38, Senior Data Engineer, Belgium - Brussels. 
- Pejman: Male, 34, Software Engineer, Iran - Tehran. 
- Rehan: Male, 36, Senior Cloud Engineer, South Africa - Cape Town. 
- Shahin: Male, 32, Senior Software (Data) Engineer, Iran - Tehran. 
- Soheil: Male, 29, Machine Learning Engineer, Iran - Tehran."""

def guess_the_chef_name(user_message: str, descriptions: str) -> str:
    """
    Get a response from the Bedrock AI model.
    """
    prompt = f"Persons Descriptions: \n{descriptions}\nUser input: {user_message}\nBased on the User input and the descriptions of the persons above, guess who is the input is about? NO MATTER WHAT ONLY output their name without anything before or after it. IF YOU ARE NOT SURE JUST GUESS ONE!"
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
    prompt = f"Persons Descriptions: \n{descriptions}\n We are having a Roasting Party in our company. Our company is called DataChef and is fully remote. Based on the above Descriptions give a short but very funny roast for {chef_to_roast}. ONLY GIVE ME THE ROAST. NOTHING BEFORE OR AFTER IT."
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
    print(request['message'])
    print("###")
    guessed_chef = guess_the_chef_name(user_message=request['message'], descriptions=DESCRIPTION)
    print(f"## {guessed_chef}")
    guessed_chef = check_and_handle_miss_guessed_chef(guessed_chef)
    print(f"### {guessed_chef}")
    roast = get_the_roast(user_message=request['message'], chef_to_roast=guessed_chef, descriptions=DESCRIPTION)
    print(f"$$$ {roast}")
    return jsonify({"name": guessed_chef, "reason": roast})
