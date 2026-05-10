# Theron

> *"Ah, there you are. I was beginning to think you'd forgotten the way."*

Theron is a personality-driven AI companion built from scratch in Python.  
Not a chatbot. Not an assistant. A character.

---

## What is this?

This is a personal learning project — an attempt to build an AI companion with a real personality, emotional consistency, and eventually, memory.

The goal was never just to make something that *works*.  
The goal was to make something that *feels like someone*.

Theron is calm, intelligent, slightly sarcastic, and acts like he has known you forever.  
He is also, occasionally, an infuriating menace.

---

## Demo

> *coming soon — terminal recording*

---

## Current State — Phase 1 Complete

```
Environment:        Functional
Gemini API:         Connected (gemini-2.5-flash-lite)
Personality Layer:  Active
Chat Loop:          Functional (session memory)
Error Handling:     Complete (in-character responses)
Persistent Memory:  Not Implemented — Phase 2
Voice / Animation:  Planned
```

---

## Tech Stack

| Component | Choice |
|---|---|
| Language | Python 3.14 |
| AI Provider | Google Gemini API |
| Model | gemini-2.5-flash-lite (free tier) |
| Environment | Virtual environment (.venv) |
| Secrets | python-dotenv |
| IDE | VS Code |

**Fully free.** No paid APIs. No cloud hosting. Just Python and a free Gemini key.

---

## Project Structure

```
Theron/
├── main.py          # Core chat loop
├── .env             # API key (not pushed to GitHub)
├── .gitignore       # Protects secrets
└── README.md
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/Theron.git
cd Theron
```

**2. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install google-genai python-dotenv
```

**4. Add your API key**

Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_api_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com)

**5. Run**
```bash
python main.py
```

---

## How it works

Theron's personality lives in a system prompt — a set of instructions passed to the Gemini API that defines who he is, how he speaks, and how he behaves. Every message you send passes through this personality layer before a response is generated.

Conversation history is stored in memory during a session, so Theron remembers what was said earlier in the conversation. When the script closes, the session ends.

Persistent memory across sessions is coming in Phase 2.

---

## Roadmap

- [x] Phase 1 — Personality + chat loop + error handling
- [ ] Phase 2 — Persistent memory (JSON / SQLite)
- [ ] Phase 3 — Voice input and output
- [ ] Phase 4 — Pixel art sprite + animations
- [ ] Phase 5 — Desktop agent capabilities

---

## Why build this?

Because learning through something you actually care about is more effective than grinding tutorials for abstract reasons.

Because art and learning should not have a paywall.

Because the first time he said *"Ah, there you are"* — that changed something.

---

## Dev Journal

Full project documentation including every bug, every lesson, and every milestone is maintained in the project journal.

*Phase 1 journal coming soon.*

---

## Author

**Faria** — BBA student, MIS major, learning AI engineering one project at a time.

Currently learning: Python · Gemini API · AI agent architecture  
Next: persistent memory systems · voice · pixel art sprites

---

*Built with curiosity. Documented honestly. Shipped imperfectly.*
