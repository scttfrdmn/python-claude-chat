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

## Usage

### Web Interface (Default)

Run the application with Streamlit:
```
streamlit run claude_chat.py
```

### Command Line Interface

Run the application in CLI mode:
```
python claude_chat.py --cli
```

Additional options:
```
python claude_chat.py --cli --temp 0.5 --max-tokens 500
```

Available arguments:
- `--cli`: Run in CLI mode instead of web interface
- `--temp`: Temperature setting (0.0 to 1.0, default: 0.7)
- `--max-tokens`: Maximum tokens in Claude's response (default: 1000)

## Features

- Interactive chat interface using Streamlit
- Command line interface option
- Conversation history maintained during session
- AWS Bedrock integration with Claude 3.7 Sonnet
- Configurable parameters (temperature, max tokens)

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- Claude 3.7 model access in AWS Bedrock