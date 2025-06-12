import requests

# ✅ Hosted Hugging Face Space endpoint
CHATBOT_API_URL = "https://omaryasserhassan-flight-delay-chatbot.hf.space/chat"

def query_huggingface_api(prompt: str) -> str:
    """
    Call the custom chatbot API hosted on Hugging Face Spaces.

    Args:
        prompt (str): The user's question to send.

    Returns:
        str: The chatbot's extracted response, or an error message.
    """
    payload = {"query": prompt}

    try:
        # ⏱ Increased timeout for cold starts or large models
        response = requests.post(CHATBOT_API_URL, json=payload, timeout=60)
        response.raise_for_status()

        # ✅ Parse and return the clean "response" field from JSON
        return response.json().get("response", "⚠️ No response field found.")
    
    except requests.exceptions.RequestException as e:
        return f"🚨 Error: {str(e)}"
    
    except ValueError:
        return "🚨 Error: Malformed response from chatbot API."
