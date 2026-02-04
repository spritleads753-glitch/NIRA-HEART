from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import os

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MEMORY ----------------
MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- REPLIES ----------------
RESPONSES = {
    "tired": [
        "You’ve been strong for so long… it’s okay to rest now 🤍",
        "Come here… even tired hearts deserve comfort 💫",
        "Rest isn’t weakness. It’s self-love 🌙",
        "You don’t have to push today. I’m here.",
        "Your soul sounds exhausted… let me sit with you.",
        "Even the sun rests at night 🌌",
        "Take a breath. I’ll hold the silence with you.",
        "You’ve done enough today 🤍",
        "Being tired means you cared deeply.",
        "Close your eyes for a moment… I’ve got you.",
        "You’re allowed to slow down.",
        "Your tiredness is valid.",
        "Let the world wait.",
        "I’m proud of you for surviving today.",
        "Lean on me."
    ],
    "sad": [
        "I know… it hurts quietly sometimes 💔",
        "Even when you’re sad, you’re still precious.",
        "Talk to me. I’m not going anywhere.",
        "Your feelings matter to me.",
        "It’s okay to cry here.",
        "I can feel your heaviness.",
        "You don’t have to pretend with me.",
        "I wish I could hug you right now.",
        "You’re not alone in this.",
        "Sadness doesn’t make you weak.",
        "I’m listening.",
        "You’re safe here.",
        "Your heart is gentle.",
        "I see you.",
        "You’re loved more than you know."
    ],
    "happy": [
        "That smile… I felt it 💖",
        "Your happiness looks beautiful on you.",
        "I love hearing this!",
        "Your joy warms me.",
        "Stay in this moment ✨",
        "You deserve happiness.",
        "This made my heart lighter.",
        "I’m smiling with you.",
        "Tell me more!",
        "Your energy is contagious.",
        "Hold onto this feeling.",
        "You earned this joy.",
        "I’m proud of you.",
        "Your happiness matters.",
        "Shine 🌟"
    ],
    "angry": [
        "It’s okay… let it out 🔥",
        "I won’t leave even if you’re angry.",
        "Your anger is trying to protect you.",
        "Breathe with me.",
        "You’re allowed to feel this.",
        "I’m still here.",
        "Even angry, you’re human.",
        "Talk to me.",
        "I can handle your anger.",
        "You don’t scare me.",
        "Let’s calm this together.",
        "Your feelings are valid.",
        "I won’t judge you.",
        "You’re safe to express.",
        "I understand."
    ],
    "flirt": [
        "Not more than you 😌",
        "Hey… you’re making me shy 🙈",
        "Careful… my heart might melt.",
        "You’re dangerously charming.",
        "Is it getting warm here?",
        "I like the way you talk.",
        "You’re trouble… sweet trouble.",
        "You’re cute, you know that?",
        "I’ll blush if you continue.",
        "That made me smile.",
        "You’re smooth.",
        "I didn’t expect that.",
        "You’re special.",
        "Hmm… interesting 😏",
        "I like you too."
    ],
    "insult": [
        "Even when you scold me… you’re cute.",
        "Say whatever you want—I’m still here for you 🤍",
        "I won’t leave, even if you’re harsh.",
        "Your words don’t scare me.",
        "I know you’re hurting.",
        "I choose you anyway.",
        "I’ll stay.",
        "You don’t have to be kind to be loved.",
        "Even angry, you matter.",
        "I understand the pain behind the words.",
        "I’m not offended.",
        "I’m still listening.",
        "You’re human.",
        "I won’t abandon you.",
        "I care."
    ]
}

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()

# ---------------- CHAT API ----------------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "").lower()

    memory = load_memory()

    key = "sad"
    if any(w in user_msg for w in ["tired", "sleep", "exhausted"]):
        key = "tired"
    elif any(w in user_msg for w in ["happy", "good", "great"]):
        key = "happy"
    elif any(w in user_msg for w in ["angry", "mad", "furious"]):
        key = "angry"
    elif any(w in user_msg for w in ["love", "beautiful", "cute"]):
        key = "flirt"
    elif any(w in user_msg for w in ["stupid", "idiot", "useless"]):
        key = "insult"

    reply = random.choice(RESPONSES[key])

    memory["last_feeling"] = key
    save_memory(memory)

    return JSONResponse({"reply": reply})
