# Claude 3.7 Chat Application

A simple Python-based chat application using Claude 3.7 via AWS Bedrock.

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
4. Edit the `.env` file with your AWS credentials and preferred region
5. Make sure you have access to Claude 3.7 in AWS Bedrock
6. Run the application:
   ```
   streamlit run claude_chat.py
   ```

## Features

- Interactive chat interface using Streamlit
- Conversation history maintained during session
- AWS Bedrock integration with Claude 3.7 Sonnet
- Configurable parameters (temperature, max tokens)

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- Claude 3.7 model access in AWS Bedrock