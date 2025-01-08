from typing import Dict, Any, Optional
import autogen
from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def log_message(self, message: str, message_type: str = "send"):
        """Log a message from this agent"""
        prefix = "🗣️" if message_type == "send" else "📩"
        log_text = f"{prefix} {self.name} ({self.role}): {message}"
        
        # Print to console
        print(log_text)
        
        # Add to Streamlit session state
        if "message_history" not in st.session_state:
            st.session_state["message_history"] = []
        st.session_state["message_history"].append(log_text)
        
        # Update the UI immediately if update function exists
        if "update_terminal" in st.session_state:
            st.session_state["update_terminal"]()
        
    def get_completion(self, messages: list) -> str:
        """Get completion from OpenAI."""
        # Log the prompt being sent
        self.log_message(messages[-1]["content"], "send")
        
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        # Log the response received
        self.log_message(content, "receive")
        
        return content

    def execute(self, *args, **kwargs):
        """To be implemented by child classes"""
        raise NotImplementedError 