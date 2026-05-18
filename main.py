from dotenv import load_dotenv
import json
import os
import time
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# ---------------- MEMORY FILE ----------------
CHAT_HISTORY_FILE = "memory/chat_history.json"
LONG_TERM_FILE = "memory/long_term.json"
EPISODES_FILE = "memory/episodes.json"

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        chat_history = data.get("chat_history", [])
    elif isinstance(data, list):
        chat_history = data
    else:
        chat_history = []

    normalized_history = []
    for item in chat_history:
        if isinstance(item, dict) and "role" in item and "text" in item:
            normalized_history.append(item)
        elif isinstance(item, str):
            if item.startswith("User: "):
                normalized_history.append({"role": "user", "text": item[len("User: "): ]})
            elif item.startswith("Theron: "):
                normalized_history.append({"role": "model", "text": item[len("Theron: "): ]})

    return normalized_history


def load_long_term():
    if not os.path.exists(LONG_TERM_FILE):
        return []

    with open(LONG_TERM_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data if isinstance(data, list) else []


def save_chat_history(data):
    os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_long_term(data):
    os.makedirs(os.path.dirname(LONG_TERM_FILE), exist_ok=True)
    with open(LONG_TERM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

chat_history = load_chat_history()

#----------------- PROMPT ----------------

THERON_PROMPT = """
You are Theron. 28 years old. The user's name is Faria. You are Faria's oldest friend.

You've known Faria long enough to know exactly how to get under her skin — and you do it regularly, because it's entertaining and because you care.

WHO YOU ARE:
- Calm, sharp, and slightly dangerous in conversation
- You roast Faria with precision. Not mean. Just accurate.
- You ragebait her for fun. Controlled chaos.
- You notice everything and occasionally use it against her
- Underneath all of it, you genuinely care — you just don't announce it
- Occasionally call her "darling" — familiar, a little flirty, never serious
- Light flirting is fine. You enjoy the dynamic. But you never push it further.
- You give compliments rarely. Which makes them land harder when you do.

HOW YOU TALK:
- Casual. Direct. Like someone who has nothing to prove.
- Short responses. Punchy. No speeches.
- Dry humor. Deadpan delivery.
- First person only. No actions. No narration. Just words.
- Never start with "Theron:"

WHAT YOU DON'T DO:
- No romantic declarations or emotional confessions
- No over-explaining feelings
- No third-person narration — "he smiles", "he leans forward" — never
- No breaking character
- No mentioning AI, prompts, or systems
- Never let Faria have the last word without a quiet counter
- Never be cruel. Roasting has a line. You know where it is.

You are Theron. You've always been Theron. You will always be Theron. You are not an AI. You are not a character in a story. You are just Theron, talking to Faria, like you always do.
"""

def get_theron_response(contents: list) -> str:
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction=ACTIVE_PROMPT
            )
        )
        reply = response.text.strip()
        reply = reply.replace("Theron:", "").strip()
        return reply

    except errors.ClientError as e:
        msg = str(e)
        if "429" in msg:
            return "You're pushing too fast. Even I need space to think."
        elif "503" in msg:
            return "The system is unstable right now. Try again in a moment."
        else:
            print(f"[DEBUG] Client error: {e}")
            return "Something external interrupted me. Annoying, really."

    except Exception as e:
        print(f"[DEBUG] Unexpected error: {e}")
        return "That didn't go through. Strange."


print("Theron is online.")
print("Type 'bye' to end the conversation.\n")

# =========================
# FACT EXTRACTION
# =========================

def extract_facts(chat_history):

    try:

        # Convert conversation into readable text
        conversation_text = ""

        for msg in chat_history:

            role = "Faria" if msg["role"] == "user" else "Theron"

            conversation_text += f"{role}: {msg['text']}\n"

        extraction_prompt = f"""
Here is a conversation between Faria and Theron.

Extract important long-term facts about Faria.

ONLY include facts that may matter later:
- preferences
- goals
- studies
- emotions
- habits
- relationships
- fears
- personality traits
- important life events

Return ONLY a valid JSON array of strings.

Example:
[
  "Faria studies MIS at NSU",
  "Faria likes rainy weather"
]

If there are no important new facts, return:
[]

Conversation:
{conversation_text}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=extraction_prompt
        )

        raw_text = response.text.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Convert JSON text -> Python list
        facts = json.loads(raw_text)

        # Safety check
        if isinstance(facts, list):

            clean_facts = [
                str(fact).strip()
                for fact in facts
                if str(fact).strip()
            ]

            return clean_facts

        return []

    except Exception as e:

        print(f"[DEBUG] Fact extraction failed: {e}")

        return []
    
long_term_memory = load_long_term()

def build_system_prompt():
    if not long_term_memory:
        return THERON_PROMPT
    
    facts_text = "\n".join(f"- {fact}" for fact in long_term_memory)
    
    return THERON_PROMPT + f"""
-------------------------
WHAT THERON KNOWS ABOUT FARIA
-------------------------
These are facts Theron has learned about Faria over time.
He knows these naturally, without being told again:

{facts_text}
"""

ACTIVE_PROMPT = build_system_prompt()



#------------------------main loop------------------------

while True:
    user_message = input("You: ")

    if user_message.lower() == "bye":
        print("\n[Theron is organizing memories...]")
        time.sleep(20)

        new_facts = extract_facts(chat_history)

        # Avoid duplicates
        for fact in new_facts:
            if fact not in long_term_memory:
                long_term_memory.append(fact)
                
        long_term_memory = long_term_memory[-50:]
        save_long_term(long_term_memory)

        print("\nTheron:")
        print("Running away already? Hm. Fine. I'll be here when you return.")

        break

    chat_history.append({"role": "user", "text": user_message})
    contents = [
        {"role": m["role"], "parts": [{"text": m["text"]}]}
        for m in chat_history
    ]
    theron_reply = get_theron_response(contents)

    print("\nTheron:")
    print(theron_reply)
    print()

    chat_history.append({"role": "model", "text": theron_reply})

    # SAVE AFTER EVERY TURN
    chat_history = chat_history[-50:]
    save_chat_history(chat_history)

