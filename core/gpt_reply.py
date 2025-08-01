from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file in project root
load_dotenv()

# Initialize OpenAI client with your API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_reply(user_message, language="en"):
    system_prompt = f"You are a helpful, polite assistant for a dental clinic in Istanbul. Answer in {language} clearly, professionally, and warmly."

    response = client.chat.completions.create(
        model="gpt-4o",  # GPT-4o mini model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

