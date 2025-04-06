import boto3
import json
import os
import argparse
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BedrockChat:
    def __init__(self):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.model_id = "anthropic.claude-3-7-sonnet-20240229-v1:0"
        
    def generate_response(self, messages, max_tokens=1000, temperature=0.7):
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            })
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body.get("content")[0].get("text")
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"

def run_cli_chat():
    """Run a CLI-based chat session with Claude 3.7"""
    chat = BedrockChat()
    messages = []
    
    print("\n=== Claude 3.7 CLI Chat ===")
    print("Type 'exit' or 'quit' to end the conversation.")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit command
        if user_input.lower() in ['exit', 'quit']:
            print("\nEnding chat session. Goodbye!")
            break
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get Claude's response
        print("\nClaude is thinking...")
        response = chat.generate_response(messages)
        
        # Print and store Claude's response
        print(f"\nClaude: {response}")
        messages.append({"role": "assistant", "content": response})

def run_streamlit():
    """Run the Streamlit web interface"""
    st.title("Claude 3.7 Chat Application")
    st.write("Chat with Claude 3.7 Sonnet through AWS Bedrock")
    
    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
            
        # Get Claude's response
        if st.session_state.messages:
            chat = BedrockChat()
            
            with st.chat_message("assistant"):
                with st.spinner("Claude is thinking..."):
                    formatted_messages = [
                        {"role": msg["role"], "content": msg["content"]} 
                        for msg in st.session_state.messages
                    ]
                    response = chat.generate_response(formatted_messages)
                    st.write(response)
                    
            # Add Claude's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    parser = argparse.ArgumentParser(description='Claude 3.7 Chat Application')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode instead of Streamlit web interface')
    parser.add_argument('--temp', type=float, default=0.7, help='Temperature (randomness) setting, 0.0 to 1.0')
    parser.add_argument('--max-tokens', type=int, default=1000, help='Maximum number of tokens in Claude\'s response')
    args = parser.parse_args()
    
    # Set global variables for model parameters
    global TEMPERATURE, MAX_TOKENS
    TEMPERATURE = args.temp
    MAX_TOKENS = args.max_tokens
    
    if args.cli:
        run_cli_chat()
    else:
        # This will use the streamlit command to run the app
        # Handled by the __name__ == "__main__" block
        run_streamlit()

if __name__ == "__main__":
    # Check if script is run directly (not through streamlit)
    if os.environ.get('STREAMLIT_RUN_PATH') is None and len(os.sys.argv) > 1:
        main()
    else:
        # Default behavior when run with streamlit
        run_streamlit()