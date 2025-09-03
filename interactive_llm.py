from llms_api import LLM_API
import yaml

def get_model_options(config,model_name):
    options = None
    for llm in config["llms"]:
        if(llm["model_name"] == model_name):
            options = llm["options"]
    if(options is None):
        raise ValueError("Default model not found in config file")
    return options



with open("config.yml", 'r') as file:
    config = yaml.safe_load(file)

model_name = input("Enter model: ")
if model_name.lower() == "":
    model_name = config["default_model"]
print(f"You entered model: {model_name}")
options = get_model_options(config, model_name)
llm_api = LLM_API(options)


system_prompt = config["system_prompt"]
while True:
    user_input = input("Enter command: ")
    print(f"You entered: {user_input}")
    user_prompt = [{"text": user_input}]
    if user_input.lower() == "exit":
        break
    #user_prompt = config["user_prompt"]
    response,usage = llm_api.openAI_call(user_prompt,system_prompt,model_name)
    #print(messages)
    print("Response:", response)
    print("Usage:", usage)

