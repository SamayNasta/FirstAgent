import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ddgs import DDGS

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def web_search(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "No results found."
    formatted = []
    for r in results:
        formatted.append(f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}")
    return "\n\n---\n\n".join(formatted)

# Define the web_search tool so Gemini knows it exists and when to use it
search_tool = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="web_search",
        description="Search the web for current, real-time information on any topic",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "query": types.Schema(
                    type=types.Type.STRING,
                    description="The search query to look up"
                )
            },
            required=["query"]
        )
    )
])

# Pass the tool to the chat session so Gemini can call it whenever needed
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

        # The model may call the search tool one or more times before giving a final answer
        # We loop until there are no more tool calls
        while True:
            tool_calls = [
                part for part in response.candidates[0].content.parts
                if hasattr(part, "function_call") and part.function_call
            ]
            if not tool_calls:
                break

            # Execute each tool call and collect the results
            tool_results = []
            for part in tool_calls:
                fc = part.function_call
                print(f"[Searching: {fc.args['query']}...]")
                result = web_search(fc.args["query"])
                tool_results.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result}
                    )
                )

            # Send results back so the model can continue
            response = chat.send_message(tool_results)

        print(f"Aria: {response.text}\n")

    except Exception as e:
        print(f"Aria: Something went wrong: {e}\n")
