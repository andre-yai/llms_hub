from openai import OpenAI
import boto3
from botocore.exceptions import ClientError
from preprocessing import create_messages
from typing import Dict, Any, Tuple, List

OPENAI_PROVIDER = "OpenAI"
BEDROCK_PROVIDER = "Bedrock"
DEFAULT_REGION = "us-east-1"
MAX_TOKENS = 512
TEMPERATURE = 0.5
TOP_P = 0.9

class LLMAPIError(Exception):
    """Custom exception for LLM API errors."""
    pass

class LLM_API:
    """
    A class to handle API calls to different LLM providers (OpenAI and AWS Bedrock).

    Attributes:
        boto_client: A boto3 client for AWS Bedrock Runtime.
        provider (str): The LLM provider (e.g., "OpenAI" or "Bedrock").
        client: An OpenAI client (if the provider is OpenAI).
    """

    def __init__(self, options: Dict[str, Any]):
        """
        Initialize the LLM_API instance.

        Args:
            options (Dict[str, Any]): A dictionary containing configuration options.
                Must include a 'provider' key.
        """
        self.provider = options.pop("provider", OPENAI_PROVIDER)
        self.boto_client = boto3.client("bedrock-runtime", region_name=DEFAULT_REGION)
        if self.provider == OPENAI_PROVIDER:
            self.client = OpenAI(**options)
        elif self.provider != BEDROCK_PROVIDER:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def call(self, user_prompt: List[Dict[str, str]], system_prompt: str, model_name: str) -> Tuple[str, Dict[str, Any]]:
        """
        Make an API call to the specified LLM provider.

        Args:
            user_prompt (List[Dict[str, str]]): The user's input prompt.
            system_prompt (str): The system prompt to guide the model's behavior.
            model_name (str): The name of the model to use.

        Returns:
            Tuple[str, Dict[str, Any]]: A tuple containing the model's response and usage information.

        Raises:
            LLMAPIError: If there's an error with the API call.
        """
        try:
            if self.provider == OPENAI_PROVIDER:
                return self._openai_call(user_prompt, system_prompt, model_name)
            elif self.provider == BEDROCK_PROVIDER:
                return self._bedrock_call(user_prompt, system_prompt, model_name)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            raise LLMAPIError(f"Error calling {self.provider} API: {str(e)}")

    def _openai_call(self, user_prompt: List[Dict[str, str]], system_prompt: str, model_name: str) -> Tuple[str, Dict[str, Any]]:
        """Make an API call to OpenAI."""
        print("OpenAI call")
        messages = create_messages(user_prompt, system_prompt)
        print(user_prompt, system_prompt, model_name)
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.model_dump()

    def _bedrock_call(self, user_prompt: List[Dict[str, str]], system_prompt: str, model_name: str) -> Tuple[str, Dict[str, Any]]:
        """Make an API call to AWS Bedrock."""
        conversation = [{"role": "user", "content": user_prompt}] 
        try:
            response = self.boto_client.converse(
                system=[{"text": system_prompt}],
                modelId=model_name,
                messages=conversation
            )
            response_text = response["output"]["message"]["content"][0]["text"]
            return response_text, response["usage"]
        except ClientError as e:
            raise LLMAPIError(f"AWS Bedrock ClientError: {str(e)}")
