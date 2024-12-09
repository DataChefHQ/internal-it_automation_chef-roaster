import boto3
import random
from botocore.exceptions import ClientError
import openai
import json
import re

def get_openai_api_key():
    secret_name = "OPENAI_API_KEY"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Fetch the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Decrypt the secret if it is encrypted
        if "SecretString" in response:
            secret = response["SecretString"]
            secret_dict = json.loads(secret)
            return secret_dict["OPENAI_API_KEY"]
        else:
            raise Exception("Secret value not found.")
    except ClientError as e:
        raise Exception(f"Error retrieving secret: {e}")
    
def read_txt_file(filename: str) -> str:
    with open(filename, 'r') as file:
        content = file.read()
    return content

openai.api_key = get_openai_api_key()
REGION = "us-east-1"
MODEL_ID = "amazon.nova-pro-v1:0" # anthropic.claude-3-sonnet-20240229-v1:0 anthropic.claude-3-5-sonnet-20240620-v1:0 anthropic.claude-3-5-sonnet-20241022-v2:0
OPENAI_MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.85
TOP_P = 0.75
MAX_LEN = 1024
MAX_INPUT_LEN = 5000
CHEFS = ["Ali", "Andrea", "Anne", "Ashkan", "Bram", "Davide", "Farbod", "Federico", "Jane", "Kiarash", "Mahdokht", "Melvyn", "Pejman", "Rehan", "Shahin", "Soheil"]
CHEFS_MAP = {
    "ali": "boy", 
    "andrea": "boy", 
    "anne": "girl", 
    "ashkan": "boy", 
    "bram": "boy", 
    "davide": "boy", 
    "farbod": "boy", 
    "federico": "boy", 
    "jane": "girl", 
    "kiarash": "boy", 
    "mahdokht": "girl",
    "melvyn": "boy", 
    "pejman": "boy", 
    "rehan": "boy", 
    "shahin": "boy", 
    "soheil": "boy"
}
DESCRIPTIONS = read_txt_file("src/prompts/descriptions.txt")
CHEFS_ROAST = {chef.lower(): read_txt_file(f"src/roasts/{chef.lower()}.txt") for chef in CHEFS}

def create_image(prompt: str) -> str:
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,  # Number of images to generate
        size="1024x1024"  # Image size options: 256x256, 512x512, or 1024x1024
    )

    image_url = response['data'][0]['url']
    print(f"Created Image with #{prompt}# with URL: {image_url}!")

    return image_url

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
    prompt = f"DataChef Roasting Party! \n\nHere's the next person: {chef_to_roast}. Some information about them:\n{descriptions}\n\nYour task: Roast {chef_to_roast}. Pick just one thing from the description to focus on, and deliver the funniest, most savage roast you can. Keep it SHORT, FUNNY, and SPICY. Do NOT try to use everything in the description—pick only ONE thing and go all in. ONLY GIVE ME THE ROAST, NOTHING ELSE!"
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

def openai_guess_the_chef_name(user_message: str, descriptions: str) -> str:
    """
    Uses OpenAI's API to guess the chef's name based on user input and descriptions.

    Args:
        user_message (str): The user's input message.
        descriptions (str): Descriptions of the persons.

    Returns:
        str: The guessed chef's name or an error message.
    """
    prompt = (
        f"Persons Descriptions:\n{descriptions}\n"
        f"User input: {user_message}\n"
        "Based on the user input and the descriptions of the persons above, "
        "guess who the input is about. NO MATTER WHAT, ONLY output their name without anything before or after it."
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_LEN,
            n=1,  # Number of responses to generate
            stop=None  # Define stop sequences if needed
        )
        # Extract and clean the response text
        response_text = response.choices[0].message.content.strip()
        return response_text
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI: {str(e)}"

def openai_get_the_roast(user_message: str, chef_to_roast: str, descriptions: str) -> str:
    """
    Uses OpenAI's API to generate a roast for the specified chef.

    Args:
        user_message (str): The user's input message.
        chef_to_roast (str): The name of the chef to roast.
        descriptions (str): Descriptions of the chef.

    Returns:
        str: The generated roast or an error message.
    """
    prompt = (
        f"DataChef Roasting Party!\n\n"
        f"Here's the next person: {chef_to_roast}. The input message: {user_message}. Some information about them:\n{descriptions}\n\n"
        f"Your task: Roast {chef_to_roast}. RANDOMLY Pick just one thing from the description to focus on, "
        "and deliver the FUNNIEST, most savage roast you can. Keep it FUNNY, and SPICY. Avoid Politics. "
        "DO NOT try to use everything in the description, PICK ONLY ONE thing and go all in. "
        "ONLY GIVE ME THE ROAST, NOTHING ELSE!"
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_LEN,
            n=1,  # Number of responses to generate
            stop=None  # Define stop sequences if needed
        )
        # Extract and clean the response text
        response_text = response.choices[0].message.content.strip()
        return response_text
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI: {str(e)}"

def openai_get_reasoning(user_message: str, descriptions: str, chef: str, random: bool) -> str:
    """
    Uses OpenAI's API to generate the reason why the chef is chosen.

    Args:
        user_message (str): The user's input message.
        descriptions (str): Descriptions of the chef.
        chef (str): The name of the chef.
        random (bool): Whether the chef is randomly chosen.
    Returns:
        str: The guessed chef's name or an error message.
    """

    descriptions = descriptions.split("*")
    chef_description = "No description"
    for description in descriptions:
        if chef.lower() in description.strip().lower()[:15]:
            chef_description = description

    prompt = (
        f"User input: {user_message}\n"
        f"Based on the user input and the descriptions of chefs we have guessed the user input is referring to {chef}\n"
        f"These are some details about {chef}: {chef_description}\n"
        f"Now you have to generate some reasoning step that why we chose {chef}. The reasoning should be logical and "
        f"related to user input but SHOULD NOT directly mention the chef, we want to make it engaging\n"
        f"Make sure to keep it VERY VERY SHORT and do NOT mention {chef} in it or their country name or city name!"
        f"Use this mapping to add if their boy or girl {CHEFS_MAP}."
    )
    if random:
        prompt += ("Start with 'Lets roast some chef with ... characteristics' like: let's roast a boy in tech world,"
                   " or let's roast a girl in dutch culture ...\nGive a VERY VERY SHORT result with just a few words")
    else:
        prompt += ("Start with 'I think' like: I think it should be a boy in tech, "
                   "or I think it's a girl with dutch culture ...\nGive a SHORT result with a few words")

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=128,
            n=1,  # Number of responses to generate
            stop=None  # Define stop sequences if needed
        )
        # Extract and clean the response text
        response_text = response.choices[0].message.content.strip()
        return response_text
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI: {str(e)}"
    
def check_and_handle_miss_guessed_chef(guessed_chef, chefs=CHEFS):
    lower_chefs = [i.lower() for i in chefs]
    if guessed_chef.lower() in lower_chefs:
        return guessed_chef.lower()
    else:
        print("Guess Randomly")
        return random.choice(chefs).lower()

def find_chef(request):
    try:
        user_message = request['prompt']
    except KeyError:
        user_message = request['message']
    if len(user_message) >= MAX_INPUT_LEN:
        user_message = request['prompt'][:MAX_INPUT_LEN]
    if user_message == "":
        user_message = "No Description Available!"

    if user_message != "No Description Available!":
        guessed_chef = openai_guess_the_chef_name(user_message=user_message, descriptions=DESCRIPTIONS)
        print(f"## {guessed_chef}")
        guessed_chef = check_and_handle_miss_guessed_chef(guessed_chef)
        print(f"### {guessed_chef}")
        reason = openai_get_reasoning(
            user_message=user_message, descriptions=DESCRIPTIONS, chef=guessed_chef, random=False
        )
    else:
        # choose randomly
        guessed_chef = check_and_handle_miss_guessed_chef("")
        print(f"#### {guessed_chef}")
        reason = openai_get_reasoning(
            user_message=user_message, descriptions=DESCRIPTIONS, chef=guessed_chef, random=True
        )

    return {"name": guessed_chef, "reason": reason}


def roast_chef(request):
    user_message = request['prompt']
    guessed_chef = request['chef']

    roast = openai_get_the_roast(
        user_message=user_message, chef_to_roast=guessed_chef, descriptions=CHEFS_ROAST[guessed_chef]
    )
    print(f"$$$ {roast}")
    return {"name": guessed_chef, "roast": roast}


def remove_chef_name_from_roast(roast: str, chefs: list, chefs_map=CHEFS_MAP):
    roast = roast.lower()
    # Loop through each chef's name in the list and remove it from the roast
    for chef in chefs:
        chef = chef.lower()
        try:
            # Use regex to replace exact matches only
            roast = re.sub(rf'\b{re.escape(chef)}\b', chefs_map[chef], roast)
        except KeyError:
            print(f"{chef} name not found")
            pass
    # Return the modified roast string
    return roast.strip()

def generate_roast_image_url(request):
    print("!!", request)
    roast = request['roast']
    roast = remove_chef_name_from_roast(roast=roast, chefs=CHEFS)

    roast_image_url = create_image(roast)

    return {"roast_image_url": roast_image_url}


if __name__ == "__main__":
    res = openai_get_reasoning("CEO", DESCRIPTIONS, "Ashkan", random=True)
    print(res)
