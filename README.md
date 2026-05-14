# Aria - AI Research Assistant

Aria is a conversational AI research assistant that searches the web in real-time to answer your questions with detailed, cited summaries.

## Features

- Conversational chat with memory — Aria remembers what you said earlier in the session
- Real-time web search — automatically searches Google when you ask about current events, prices, rates, or news
- Cited sources — always provides URLs so you can verify the information
- Powered by Google Gemini 2.5 Flash with built-in Google Search

## Tech Stack

- **Python**
- **Google Gemini 2.5 Flash** — the AI model with built-in Google Search grounding
- **google-genai** — official Google Gemini SDK
- **python-dotenv** — loads API keys from a `.env` file

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SamayNasta/FirstAgent.git
cd FirstAgent
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install google-genai python-dotenv
```

### 4. Add your API key

Create a `.env` file in the root of the project:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com).

### 5. Run the agent

```bash
python agent.py
```

## Usage

```
Aria is ready! Type 'quit' to exit.

You: What is the USD to INR rate today? Cite your source.
Aria: The current USD to INR rate is ...

You: quit
Goodbye!
```

## How It Works

1. You type a message
2. Gemini reads the message and decides if a web search is needed
3. If yes, it searches Google automatically using its built-in Search Grounding tool
4. Gemini summarizes the results and responds with cited sources
5. The conversation history is maintained throughout the session
