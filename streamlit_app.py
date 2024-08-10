import sys
try:
    from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
except ImportError:
    #  pip    install      git+https://github.com/microsoft/autogen.git@gemini
    #  pip    install      git+https://github.com/microsoft/autogen.git@gemini-vision
    sys.process.exec([sys.executable, "-m", "pip", "install", "autogen@gemini", "autogen@gemini-vision"])
import streamlit as st
import os

# Set your Google API key here
api_key = os.getenv("API_KEY")

# Define the config_list directly
config_list = [
    {
        "model": "gemini-pro",
        "api_key": api_key,
    },
    {
        "model": "gemini-pro-vision",
        "api_key": api_key,
    },
]

# Initialize agents
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
assistant = AssistantAgent(
    "assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0.2,
        "max_tokens": 80000,
    },
)

# Streamlit app title
st.title("Gemini Auto Agent App")

# User input
user_input = st.text_area("Enter your request:")

# Run agents and display output
if st.button("Run"):
    user_proxy.initiate_chat(assistant, message=user_input)
    st.write("**Assistant:**")
    st.write(assistant.last_message["content"])

    # Display code if generated
    if "code_blocks" in assistant.last_message:
        for code_block in assistant.last_message["code_blocks"]:
            st.code(code_block, language=code_block["language"])