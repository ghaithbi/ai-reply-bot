import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gpt_reply import get_gpt_reply

test_message = "Hi, how much do dental implants cost?"

reply = get_gpt_reply(test_message, language="en")

print("💬 Client Message:")
print(test_message)
print("\n🤖 AI Reply:")
print(reply)


