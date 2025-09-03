# LLMs Hub

This project is a hub for working with Large Language Models (LLMs). It provides tools for evaluation, preprocessing, and interactive use of various LLMs, including OpenAI models and Amazon Bedrock.

## Project Structure

- `interactive_llm.py`: Interactive script for using LLMs
- `llms_api.py`: API interface for LLMs (OpenAI and Amazon Bedrock)
- `preprocessing.py`: Data preprocessing utilities
- `config.yml`: Configuration file for LLMs

## Recent Improvements

The project has undergone significant improvements:

1. Enhanced error handling and type checking
2. Improved code organization and readability
3. Added support for both OpenAI and Amazon Bedrock LLMs
4. Implemented more robust preprocessing for text and image inputs

## How to Use the Interactive Python Script

To use the interactive Python script:

1. Ensure you have all the necessary dependencies installed.
2. Configure your `config.yml` file with the necessary API keys and model settings.
3. Run the script using Python:

   ```
   python interactive_llm.py
   ```

4. Follow the prompts to interact with the LLM of your choice.
5. Your conversation will be automatically saved to Amazon S3 for later reference.

### Saving Conversations to Amazon S3

The LLMs Hub now includes a feature to save your conversations to Amazon S3 for later reference. This allows you to review past interactions and analyze the performance of different models over time.

To set up S3 storage:

1. Ensure you have an AWS account and have set up the AWS CLI with your credentials.
2. In your `config.yml` file, add the following S3 configuration:

   ```yaml
   s3_config:
     bucket_name: your-bucket-name
     region_name: your-aws-region
   ```

3. Replace `your-bucket-name` with the name of your S3 bucket and `your-aws-region` with the appropriate AWS region.

Each conversation will be saved as a separate JSON file in your specified S3 bucket, with a timestamp as the filename. You can access these files using the AWS Management Console or AWS CLI.

Note: Make sure your AWS credentials have the necessary permissions to write to the specified S3 bucket.

## Configuring a New LLM

To configure a new LLM in the `config.yml` file:

1. Open the `config.yml` file in a text editor.
2. Add a new entry for your LLM under the `llms:` section.
3. Specify the required parameters for your LLM, which include:
   - `model_name`: A unique identifier for your LLM
   - `provider`: The LLM provider (e.g., "OpenAI" or "Bedrock")
   - `options`: Any additional parameters required by the LLM

Example:

```yaml
llms:
  - model_name: gpt-4
    provider: OpenAI
    options:
      api_key: your_openai_api_key_here
  - model_name: claude-v2
    provider: Bedrock
    options:
      region_name: us-east-1
```

4. Save the `config.yml` file after making your changes.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/andre-yai/llms_hub.git
   cd llms_hub
   ```

2. Set up a Python virtual environment (recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your `config.yml` file with the necessary API keys and model settings.

5. If you plan to use Amazon Bedrock:
   a. Install the AWS CLI:
      ```
      pip install awscli
      ```
   b. Configure AWS CLI with your credentials:
      ```
      aws configure
      ```
      Follow the prompts to enter your AWS Access Key ID, Secret Access Key, and default region.

6. You're ready to use the LLMs Hub!

## Contributing

Contributions to the LLMs Hub project are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure your code adheres to the project's coding standards, includes appropriate type hints, and has proper error handling.

## Future Enhancements

We have plans to further enhance this project in the following areas:

1. Functionality: Support for more LLM providers and types of LLM tasks
2. Performance and Scalability: Asynchronous API calls and caching mechanisms
3. User Experience: Web-based GUI and CLI interface
4. Development Workflow: CI/CD pipeline and improved testing
5. Documentation: Expanded usage examples and API documentation

Stay tuned for these exciting improvements!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
