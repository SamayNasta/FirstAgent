import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini has a built-in Google Search tool — no external search library needed
# When enabled, the model automatically searches Google whenever it needs current information
search_tool = types.Tool(google_search=types.GoogleSearch())

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are Aria, a research assistant. When answering questions, search the web to find accurate and up-to-date information. Provide detailed, well-structured summaries of what you find. Always cite your sources with URLs. Search multiple times if a question has multiple parts.",
        tools=[search_tool]
    )
)

print("Aria is ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    try:
        response = chat.send_message(user_input)
        print(f"Aria: {response.text}\n")
    except Exception as e:
        print(f"Aria: Something went wrong: {e}\n")
