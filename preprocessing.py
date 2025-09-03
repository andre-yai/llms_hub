def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return "data:image/png;base64," + encoded_string


def create_messages(user_prompts,system_prompt=""):
    system_message = {"role": "system", "content": [{"type": "text", "text": system_prompt}]}
    user_messages = {"role": "user", "content": []}
    
    for prompts in user_prompts:
        print("prompts:", prompts)
        for option, text_value in prompts.items():
            print(option, text_value)
            if option == "text":
                user_message = {"type": "text", "text": text_value}
            elif option == "image":
                image_path = text_value
                user_message = {"type": "image_url","image_url": {"url": get_image_base64(image_path)}}
            user_messages["content"].append(user_message)

    return [system_message, user_messages]

