# Use the native inference API to send a text message to Meta Llama 3.

import json

import boto3
from botocore.exceptions import ClientError
from g4f.client import Client
from groq import Groq
from util.const import SYSTEM_PROMPT,GROQ_API

# Create a Bedrock Runtime client in the AWS Region of your choice.
# client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Set the model ID, e.g., Llama 3 8b Instruct.
model_id = "meta.llama3-8b-instruct-v1:0"


class AI:
    def __init__(self, model_id: str="meta.llama3-8b-instruct-v1:0"):
        self.model_id = model_id
        
    def ask_g4(self,prompt:str)->str:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        resp = response.choices[0].message.content
        return resp
        
    def ask_g4f(self,prompt:str)->str:
        client = Groq(
            api_key=GROQ_API,
        )
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
        )
        resp = response.choices[0].message.content
        return resp



    def ask_llama(self,prompt:str)->str:
        """
        Ask Llama 3 a question.
        """ 
        # Embed the prompt in Llama 3's instruction format.
        formatted_prompt = f"""
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>{SYSTEM_PROMPT}<|eot_id|>
        <|start_header_id|>user<|end_header_id|>The context is as follows:{prompt}<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        print(formatted_prompt)
        
        # Format the request payload using the model's native structure.
        native_request = {
            "prompt": formatted_prompt,
            "max_gen_len": 512,
            "temperature": 0.5,
        }
        
        # Convert the native request to JSON.
        request = json.dumps(native_request)
        
        try:
            # Invoke the model with the request.
            response = client.invoke_model(modelId=self.model_id, body=request)
        
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)
        
        # Decode the response body.
        model_response = json.loads(response["body"].read())
        
        # Extract and print the response text.
        response_text = model_response["generation"]
        # print(response_text)
        return response_text
    



