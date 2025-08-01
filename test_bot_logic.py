# test_bot_logic.py
import os
from bot_logic import qa_chain

print("--- Starting AI Logic Test ---")

# Check if the OpenAI API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    print("\nERROR: OPENAI_API_KEY is not set!")
    print("Please create a file named '.env' and add the following line:")
    print("OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
else:
    print("✅ OpenAI API Key found.")
    print("\nSending a test question to the AI...")
    try:
        test_question = "hello"
        response = qa_chain.invoke({"question": test_question})
        answer = response.get("answer")

        if answer:
            print(f"✅ AI responded successfully!")
            print(f"Bot's Answer: {answer}")
        else:
            print("ERROR: AI responded, but the answer was empty.")

    except Exception as e:
        print(f"\nERROR: The AI chain failed with an error: {e}")

print("\n--- Test Complete ---")


