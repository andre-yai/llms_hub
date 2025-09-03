from llms_api import LLM_API
import yaml
from typing import Dict, Any
import boto3
import json
from datetime import datetime

CONFIG_FILE = "config.yml"
EXIT_COMMAND = "exit"

def get_model_options(config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """
    Retrieve the options for a specific model from the configuration.

    Args:
        config (Dict[str, Any]): The configuration dictionary containing LLM settings.
        model_name (str): The name of the model to retrieve options for.

    Returns:
        Dict[str, Any]: The options for the specified model.

    Raises:
        ValueError: If the specified model is not found in the configuration.
    """
    for llm in config["llms"]:
        if llm["model_name"] == model_name:
            return llm["options"]
    raise ValueError(f"Model '{model_name}' not found in config file")

def load_config(file_path: str) -> Dict[str, Any]:
    """
    Load the configuration from a YAML file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: The loaded configuration.

    Raises:
        yaml.YAMLError: If there's an error parsing the YAML file.
        FileNotFoundError: If the config file is not found.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        raise
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
        raise

def save_conversation_to_s3(model_name: str, system_prompt: str, conversation: list, bucket_name: str = None):
    """
    Save the conversation to an S3 bucket.

    Args:
        model_name (str): The name of the model used.
        system_prompt (str): The system prompt used.
        conversation (list): The conversation history.

    Note:
        This is a placeholder function. Implement actual S3 saving logic as needed.
    """
    print("Saving conversation to S3...")
    # Implement actual S3 saving logic here
    # For example, using boto3 to upload the conversation to a specified S3 bucket
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    key = f"conversations/{model_name}_conversation_{timestamp}.json"

    conversation_data = {
        "model_name": model_name,
        "system_prompt": system_prompt,
        "conversation": conversation
    }

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(conversation_data),
            ContentType="application/json"
        )
        print(f"Conversation saved to S3 bucket '{bucket_name}' with key '{key}'.")
    except Exception as e:
        print(f"Failed to save conversation to S3: {e}")


def main():
    try:
        config = load_config(CONFIG_FILE)
        
        use_specific_model = input("Do you want to use a specific model? (yes/no): ").strip().lower()
        if use_specific_model == "yes":
            model_name = input("Enter model: ").strip()
            if not model_name:
                print("No model entered. Using default model.")
                model_name = config["default_model"]
        else:
            model_name = config["default_model"]
        print(f"Using model: {model_name}")
        
        options = get_model_options(config, model_name)
        llm_api = LLM_API(options)
        
        custom_prompt = input("Do you want a custom system prompt? (yes/no): ").strip().lower()
        if custom_prompt == "yes":
            system_prompt = input("Enter your custom system prompt: ").strip()
        else:
            system_prompt = config["system_prompt"]
        print(f"System prompt set to: {system_prompt}")
        
        conversation = []

        system_prompt = config["system_prompt"]

        while True:
            user_input = input("Enter text: ").strip()
            print(f"You entered: {user_input}")
            # Save user input and model response to conversation history
            if user_input.lower() == EXIT_COMMAND:
                save_choice = input("Do you want to save the conversation for later reference? (yes/no): ").strip().lower()
                if save_choice == "yes":
                    save_conversation_to_s3(model_name, system_prompt, conversation, config["bucket_name"])
                save_conversation_to_s3(model_name, system_prompt, conversation)
                break

            user_prompt = [{"text": user_input}]
            try:
                response, usage = llm_api.call(user_prompt, system_prompt, model_name)
                conversation.append({"user": user_input, "response": response, "usage": usage})
                print("Response:", response)
                print("Usage:", usage)
            except Exception as e:
                print(f"Error during API call: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
