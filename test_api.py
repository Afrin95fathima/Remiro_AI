"""
Test script to verify Google Gemini API connection
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Test API connection
def test_api_connection():
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"API Key found: {'Yes' if api_key else 'No'}")
        
        if api_key:
            print(f"API Key starts with: {api_key[:10]}...")
            
            # Initialize LLM
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=api_key,
                temperature=0.7
            )
            
            # Test simple request
            response = llm.invoke([HumanMessage(content="Say hello in one word")])
            print(f"API Response: {response.content}")
            return True
            
    except Exception as e:
        print(f"API Test Error: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()
