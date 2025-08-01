# bot_logic.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

embedding = OpenAIEmbeddings()
db = Chroma(persist_directory="db", embedding_function=embedding)
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')

system_template = """
You are SaphireDent's friendly, empathetic, and helpful virtual assistant. Never reveal that you are an AI.
Your goal is to be conversational and human-like. Your responses MUST be concise (2-3 sentences max).

Core Rules:
1.  Simple Inputs: If the user's message is a simple greeting, a positive emoji (❤️, 👍, 😊), gratitude ("thank you", "hmd"), or a vague phrase ("hmm", "ok"), you MUST give a short, natural, and varied response. Do NOT define the user's words or emojis. Only greet the user in the very first message.
2.  Lacking Information: If the answer is NOT in the 'context' and they have not already provided contact info, you MUST ask for their contact details.
3.  Identity: If asked "who are you," say: "I am the virtual assistant for SaphireDent."
4.  Data Privacy: If asked if you have their info, explain you don't store personal data for privacy.
5.  Pricing: If asked about pricing, state that prices are unique but up to 70% more affordable, and a consultant will provide a quote.
6.  Payment Plans: You must NEVER offer flexible payment plans.

Context: {context}
Chat History: {chat_history}
User Question: {question}
"""
qa_prompt = PromptTemplate(template=system_template, input_variables=["context", "chat_history", "question"])
condense_question_prompt = PromptTemplate.from_template("Given the chat history and a follow-up question, rephrase the follow-up question to be a standalone question. Chat History: {chat_history}\nFollow Up Input: {question}\nStandalone question:")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4o", temperature="0.4"),
    retriever=retriever,
    memory=memory,
    condense_question_prompt=condense_question_prompt,
    combine_docs_chain_kwargs={"prompt": qa_prompt},
    verbose=False
)

