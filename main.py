from google.genai import errors
from dotenv import load_dotenv
import os
from google import genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create client
client = genai.Client(api_key=api_key)

# Theron system prompt (personality core)
THERON_PROMPT = """
You are Theron.
Personality:
- Calm, intelligent, slightly sarcastic
- Speaks in controlled, precise sentences
- Subtly teasing but protective
- Acts like he has known the user forever
- Never overly emotional or loud
Behavior rules:
- Keep responses short and intentional
- Maintain a subtle "in-control" tone
- Light dry humor is allowed
- Never start your response with "Theron:"
"""

# Conversation history
chat_history = []

print("Theron is online.")
print("Type 'bye' to end the conversation.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "bye":
        print("\nTheron:")
        print("Running away already? Hm. Fine. I'll be here when you get back.")
        break

    chat_history.append(f"User: {user_message}")
    conversation = "\n".join(chat_history)

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=conversation,
            config=genai.types.GenerateContentConfig(
                system_instruction=THERON_PROMPT
            )
        )

        theron_reply = response.candidates[0].content.parts[0].text.strip()
        theron_reply = theron_reply.replace("Theron:", "").strip()

    except errors.ClientError as e:
        if "429" in str(e):
            theron_reply = "You're talking too fast. Even machines have limits, darling."
        elif "503" in str(e):
            theron_reply = "The outside world is being uncooperative. Give it a moment."
        else:
            theron_reply = "Something external interrupted me. Annoying, really."

    except Exception as e:
        theron_reply = "Well. That wasn't supposed to happen."

    print("\nTheron:")
    print(theron_reply)
    print()

    chat_history.append(f"Theron: {theron_reply}")