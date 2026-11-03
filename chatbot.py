import os
from groq import Groq
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")

MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")

SYSTEM_PROMPT = """You are a helpful, honest and concise AI assistant."""

client = Groq(api_key=GROQ_API_KEY)

class State(TypedDict):
    user_input: str
    response: str
    
def chatbot_node(state: State) -> dict:
    """"Send the user's message to the LLM and store the reply in state."""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": state["user_input"]
                }
            ]
        )
        
        reply = completion.choices[0].message.content
    except Exception as error:
        reply = f"Sorry, something went wrong: {error}"
    
    return {
        "response": reply
    }
    
builder = StateGraph(State)
builder.add_node("chatbot_node", chatbot_node)

builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

def get_response(user_input: str) -> str:
    """Run the graph and return the reply."""
    response = graph.invoke({
        "user_input": user_input
    })
    
    return response["response"]

print(get_response("Hello"))