import streamlit as st
import pandas as pd
import json
import os
from llms_api import LLM_API
import yaml
from typing import Dict, Any

CONFIG_FILE = "config.yml"


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


def save_settings(model, system_prompt):
    settings = {
        "model": model,
        "system_prompt": system_prompt
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"model": "gpt-3.5-turbo", "system_prompt": "You are a helpful assistant."}

def main():
    st.title("Interactive LLM Conversation")

    # Load config and saved settings
    config = load_config(CONFIG_FILE)
    saved_settings = load_settings()

    # Sidebar for model and system prompt setup
    st.sidebar.header("Setup")
    model_options = [llm["model_name"] for llm in config["llms"]]
    default_index = model_options.index(saved_settings["model"]) if saved_settings["model"] in model_options else 0
    model = st.sidebar.selectbox("Select Model", model_options, index=default_index)
    system_prompt = st.sidebar.text_area("System Prompt", value=saved_settings["system_prompt"])

    # Save settings button
    if st.sidebar.button("Save Settings"):
        save_settings(model, system_prompt)
        st.sidebar.success("Settings saved successfully!")

    # Display current settings
    st.sidebar.subheader("Current Settings")
    st.sidebar.write(f"Model: {model}")
    st.sidebar.write(f"System Prompt: {system_prompt}")

    options = get_model_options(config, model)
    # Initialize LLM_API
    llm_api = LLM_API(options)

    # Initialize or load conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display conversation history
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to conversation
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            user_input_text = [{"text": user_input}]
            st.write(user_input)

        # Get LLM response
        with st.spinner("Thinking..."):
            response, _ = llm_api.call(
                user_prompt=user_input_text,
                system_prompt=system_prompt,
                model_name=model
            )

        # Add assistant response to conversation
        st.session_state.conversation.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
