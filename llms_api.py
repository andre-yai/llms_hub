from openai import OpenAI
import boto3
from botocore.exceptions import ClientError
from preprocessing import create_messages

class LLM_API:
    def __init__(self, options):
        # Create a Bedrock Runtime client in the AWS Region you want to use.
        self.boto_client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.provider = options["provider"]
        del options["provider"]
        if self.provider == "OpenAI":
            self.client = OpenAI(**options)
        

    def openAI_call(self, user_prompt,system_prompt, model_name):
        # This is a placeholder function. Replace with actual OpenAI API call.
        if self.provider == "OpenAI":
            messages = create_messages(user_prompt,system_prompt)
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            print(response)
            return response.choices[0].message,response.usage
        else:
            try:
                # Send the message to the model, using a basic inference configuration.
                conversation = [
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ]
                response = self.boto_client.converse(
                    system=[{"text": system_prompt}],
                    modelId=model_name,
                    messages=conversation,
                    inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
                )

                # Extract and print the response text.
                response_text = response["output"]["message"]["content"][0]["text"]
                return response_text,response["usage"]
        
            except (ClientError, Exception) as e:
                print(f"ERROR: Can't invoke '{model_name}'. Reason: {e}")
                exit(1)



# if __name__ == "__main__":
#     secret_api_key = "your_openai_api_key_here"
#     llm_api = LLM_API(secret_api_key)
#     client = llm_api.client

#     system_prompt = "You are a helpful assistant."
#     user_prompt = {"text": "Hello, how can you assist me today?"}
#     model_name = "gpt-5"
#     messages = create_messages(user_prompt,system_prompt)
#     response,usage = llm_api.openAI_call(messages,model_name)

#     print("Response:", response.content)
#     print("Usage:", usage)
