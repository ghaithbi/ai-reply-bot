# ask_gpt.py
from bot_logic import qa_chain

print("🤖 SaphireDent Assistant (Local Test) is online.")
while True:
    question = input("\n💬 Ask something (or type 'exit'): ")
    if question.lower() in ["exit", "quit"]:
        break

    response = qa_chain.invoke({"question": question})
    print("🤖 Answer:", response["answer"])

