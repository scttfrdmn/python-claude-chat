import boto3
import json
import os
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

def main():
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

if __name__ == "__main__":
    main()