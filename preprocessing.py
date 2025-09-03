import base64
from typing import List, Dict, Any
import os

DATA_URI_PREFIX = "data:image/png;base64,"
TEXT_TYPE = "text"
IMAGE_TYPE = "image"
IMAGE_URL_TYPE = "image_url"

class PreprocessingError(Exception):
    """Custom exception for preprocessing errors."""
    pass

def get_image_base64(image_path: str) -> str:
    """
    Convert an image file to a base64-encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: A base64-encoded string representation of the image,
             prefixed with the appropriate data URI scheme.

    Raises:
        PreprocessingError: If there's an error reading or encoding the image.
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return DATA_URI_PREFIX + encoded_string
    except Exception as e:
        raise PreprocessingError(f"Error processing image {image_path}: {str(e)}")

def create_messages(user_prompts, system_prompt: str = "") -> List[Dict[str, Any]]:
    """
    Create a list of messages for the LLM API call, including system and user messages.

    Args:
        user_prompts (Union[str, List[Dict[str, str]]]): Either a single string prompt or a list of dictionaries containing user prompts.
            If a list, each dictionary should have either a 'text' or 'image' key.
        system_prompt (str, optional): The system prompt to guide the model's behavior.
            Defaults to an empty string.

    Returns:
        List[Dict[str, Any]]: A list containing two dictionaries - the system message and user messages.

    Raises:
        PreprocessingError: If there's an error processing the prompts.

    Note:
        This function handles both text and image inputs in the user prompts.
        For image inputs, it converts the image to a base64-encoded string.
    """
    try:
        system_message = {"role": "system", "content": [{"type": TEXT_TYPE, "text": system_prompt}]}
        user_messages = {"role": "user", "content": []}
        
        if isinstance(user_prompts, str):
            user_messages["content"].append({"type": TEXT_TYPE, "text": user_prompts})
        elif isinstance(user_prompts, list):
            for prompts in user_prompts:
                option, value = next(iter(prompts.items()))
                if option == TEXT_TYPE:
                    user_messages["content"].append({"type": TEXT_TYPE, "text": value})
                elif option == IMAGE_TYPE:
                    user_messages["content"].append({
                        "type": IMAGE_URL_TYPE,
                        IMAGE_URL_TYPE: {"url": get_image_base64(value)}
                    })
                else:
                    raise ValueError(f"Unsupported prompt type: {option}")

        return [system_message, user_messages]
    except Exception as e:
        raise PreprocessingError(f"Error creating messages: {str(e)}")
