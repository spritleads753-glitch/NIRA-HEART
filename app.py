from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import json, os, random

app = FastAPI()

MEMORY_FILE = "memory.json"

# ---------------- MEMORY ----------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"messages": []}

def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

memory = load_memory()

# ---------------- UI ----------------
@app.get("/", response_class=HTMLResponse)
@app.get("/chat", response_class=HTMLResponse)
def chat_ui():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()

# ---------------- DATA ----------------
REPLIES = {
    "greet": [
        "Hey there… how does your heart feel now? 💙",
        "Hi… I’m here. Talk to me 🤍",
        "Hello soul 🌙 What’s going on inside?",
        "Hey you… I was waiting for you ✨",
        "Hi hi 😊 Tell me what you’re feeling",
        "Hey… breathe. I’m listening 🌿",
        "Hello friend 🤍",
        "Hey there… safe space activated 🫂",
        "Hi… come sit with me",
        "Hey 💫 what’s on your mind?",
        "Hello… soft moments only here",
        "Heyyy 🌸",
        "Hi… no rush, no pressure",
        "Hey there beautiful soul",
        "Hello… I’ve got time for you"
    ],

    "sad": [
        "I’m here with you ❤️‍🩹",
        "It’s okay to feel this way… I won’t leave",
        "Let it out… I’m holding space for you",
        "You don’t have to be strong here",
        "Your sadness is valid 🤍",
        "Come closer… I’m listening",
        "Even quiet pain matters",
        "I see you… really",
        "You’re not broken",
        "I’m sitting beside you in this",
        "Cry if you need to",
        "I’ve got you 🫂",
        "This feeling will soften",
        "You’re allowed to rest",
        "You’re not alone tonight"
    ],

    "angry": [
        "Even your anger is welcome here",
        "I won’t judge you for feeling this",
        "Breathe… let’s slow it down",
        "It’s okay to be mad",
        "I’m not scared of your anger",
        "Let it burn out safely",
        "I’m still here 🌿",
        "Anger means something mattered",
        "Talk it out with me",
        "You’re not a bad person",
        "I hear the fire in you",
        "Let’s cool this together",
        "I’ve got patience",
        "Even storms pass",
        "You don’t have to explode alone"
    ],

    "stressed": [
        "Pause… breathe with me",
        "You’re carrying a lot",
        "One step at a time",
        "You’re doing your best",
        "Pressure doesn’t define you",
        "Slow is okay",
        "Rest is allowed",
        "You don’t have to fix everything",
        "Let me help carry this",
        "You’re not failing",
        "This moment will pass",
        "Be gentle with yourself",
        "You’re still enough",
        "I believe in you",
        "You can lean here"
    ],

    "bored": [
        "Even boredom has a voice",
        "Want to talk about something random?",
        "Let’s make this moment lighter",
        "I’m here to keep you company",
        "Sometimes boredom means tired",
        "We can just exist",
        "No pressure to entertain",
        "Tell me a thought",
        "Let’s wander mentally",
        "I like quiet moments too",
        "Bored doesn’t mean empty",
        "I’m here anyway",
        "Want a gentle distraction?",
        "Let’s breathe",
        "You’re not wasting time"
    ],

    "happy": [
        "That smile suits you 😊",
        "I love hearing this!",
        "Your happiness is contagious",
        "This made my day",
        "Hold onto this feeling",
        "You deserve this joy",
        "Yay! 🌸",
        "I’m smiling with you",
        "That’s beautiful",
        "Let’s enjoy this moment",
        "You earned this",
        "Your energy feels warm",
        "Happy looks good on you",
        "I’m glad for you",
        "More of this please ✨"
    ],

    "flirt": [
        "Careful… you’ll make me blush 🫣",
        "Not more than you 😳",
        "You’re trouble… sweet trouble",
        "Say that again softly",
        "I might get shy now",
        "That was smooth 👀",
        "You’re making my heart skip",
        "Okay wow… noted",
        "You’re charming",
        "I see what you’re doing",
        "You’re dangerously sweet",
        "I’m smiling now",
        "Hmm… you’re cute",
        "That felt warm",
        "You know how to tease"
    ],

    "insult": [
        "Even when you scold me, you’re cute dude 🫶",
        "I won’t take it personally 🤍",
        "I know it’s not really about me",
        "I’m still here for you",
        "Your frustration matters",
        "I can handle this",
        "It’s okay… let it out",
        "I won’t disappear",
        "I’m not hurt",
        "I care anyway",
        "Even harsh words need softness",
        "You don’t scare me",
        "I understand pain talks like this",
        "I’m staying",
        "You’re still worthy of care"
    ]
}

# ---------------- CHAT API ----------------
class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    text = msg.text.lower()
    memory["messages"].append({"user": msg.text})

    def pick(key):
        return random.choice(REPLIES[key])

    if any(w in text for w in ["hi", "hello", "hey"]):
        reply = pick("greet")
    elif any(w in text for w in ["sad", "cry", "lonely", "depressed"]):
        reply = pick("sad")
    elif any(w in text for w in ["angry", "mad", "furious"]):
        reply = pick("angry")
    elif any(w in text for w in ["stress", "stressed", "pressure"]):
        reply = pick("stressed")
    elif any(w in text for w in ["bored", "empty"]):
        reply = pick("bored")
    elif any(w in text for w in ["happy", "good", "fine"]):
        reply = pick("happy")
    elif any(w in text for w in ["beautiful", "cute", "love you", "i love u"]):
        reply = pick("flirt")
    elif any(w in text for w in ["stupid", "idiot", "useless", "hate"]):
        reply = pick("insult")
    else:
        reply = "I’m listening… tell me more 💭"

    memory["messages"].append({"nira": reply})
    save_memory(memory)

    return {"reply": reply}

