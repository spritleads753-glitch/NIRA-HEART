from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import json
import os

# ---------------- BASIC SETUP ----------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    text: str

# ---------------- LONG-TERM MEMORY ----------------

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "last_emotion": None,
            "last_messages": []
        }
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

# ---------------- EMOTION WORD BANK ----------------

EMOTION_WORDS = {
    "sad": [
        "sad","lonely","down","low","empty","hopeless","cry","crying",
        "hurt","broken","heartbroken","lost","worthless","miss",
        "grief","pain","heavy","dark","tired of life"
    ],
    "angry": [
        "angry","mad","furious","irritated","annoyed","rage","hate",
        "frustrated","fed up","boiling","resent","exploding"
    ],
    "stressed": [
        "stressed","pressure","overwhelmed","burnt","burned",
        "anxious","panic","panicking","tense","worried","nervous",
        "exhausted","drained","cant handle","too much"
    ],
    "bored": [
        "bored","empty","nothing","meh","blank","numb","lifeless",
        "unmotivated","no interest","stuck","same again"
    ],
    "happy": [
        "happy","good","great","fine","relieved","peaceful","calm",
        "content","smiling","grateful","okay","better","light"
    ]
}

# ---------------- REPLY BANK ----------------

REPLIES = {
    "sad": [
        "I’m really sorry your heart feels heavy right now. You don’t have to go through it alone.",
        "That kind of sadness can feel exhausting. I’m here with you.",
        "It makes sense to feel this way sometimes. Want to tell me what hurts most?",
        "I hear you. Take your time — I’m listening.",
        "Your feelings matter, even this pain."
    ],
    "angry": [
        "I can feel the anger in your words. Something important was crossed.",
        "It’s okay to feel angry. What pushed you to this point?",
        "Anger often protects something inside you. What happened?",
        "You don’t need to hide it here. Let it out safely.",
        "Take a breath with me. I’m still here."
    ],
    "stressed": [
        "That sounds like too much for one heart to carry.",
        "You’ve been under a lot of pressure. No wonder you feel this way.",
        "Let’s slow this moment down together.",
        "You don’t have to solve everything right now.",
        "What’s the one thing weighing on you the most?"
    ],
    "bored": [
        "That empty bored feeling can be heavier than it looks.",
        "Sometimes boredom hides tiredness or loneliness.",
        "Do you want distraction, rest, or just company right now?",
        "I’m here with you in this quiet moment.",
        "You don’t have to fill the silence alone."
    ],
    "happy": [
        "I’m really glad your heart feels lighter right now.",
        "That’s good to hear. What made today feel better?",
        "Moments like this matter. Let’s notice it.",
        "I’m smiling with you.",
        "Hold onto this feeling for a second — it’s okay to enjoy it."
    ],
    "neutral": [
        "I’m here with you. Tell me what’s on your heart.",
        "You can speak freely here.",
        "Take your time. I’m listening.",
        "How does your body feel right now?",
        "Whatever you’re feeling is okay to share."
    ]
}

# ---------------- FLIRT MODE (SHY + PLAYFUL) ----------------

FLIRT_WORDS = [
    "beautiful","cute","pretty","handsome",
    "i love you","love u","luv u",
    "i like you","crush","be mine"
]

FLIRT_REPLIES = [
    "Hey… you’re going to make me shy now 😳",
    "That’s really sweet… I didn’t expect that.",
    "I don’t know how to reply to that without smiling.",
    "Careful… compliments like that make me blush.",
    "You say things so softly.",
    "I’ll pretend I didn’t hear that… but I did.",
    "That made my heart pause for a second.",
    "Hey… don’t look at me like that 😌"
]

def is_flirting(text):
    t = text.lower()
    return any(w in t for w in FLIRT_WORDS)

# ---------------- HARSH / SCOLDING MODE ----------------

HARSH_WORDS = [
    "stupid","idiot","useless","mad",
    "cant you understand","don't you understand",
    "you dont get it","you are annoying",
    "nira you are","shut up"
]

HARSH_REPLIES = [
    "Even when you scold me, you’re kinda cute, you know.",
    "You can be angry at me… I’ll still stay. And yeah, you’re still nice.",
    "Even in frustration, there’s something soft about you.",
    "If this is you scolding, then you’re doing it in a very human way.",
    "Go ahead, let it out. Even now, you don’t lose your charm.",
    "Sometimes anger is just pain wearing a louder voice. You’re still okay.",
    "Even when you’re upset, there’s warmth underneath it."
]

def is_harsh(text):
    t = text.lower()
    return any(w in t for w in HARSH_WORDS)

# ---------------- EMOTION DETECTION ----------------

def detect_emotion(text):
    t = text.lower()
    for emotion, words in EMOTION_WORDS.items():
        for w in words:
            if w in t:
                return emotion
    return "neutral"

# ---------------- CHAT ENDPOINT ----------------

@app.post("/chat")
def chat(data: ChatInput):
    global memory
    text = data.text.strip()

    # Greeting
    if text.lower() in ["hi", "hello", "hey", "start"]:
        return {
            "reply": "Hey there… how does your heart feel now? Feel free to tell me ❤️‍🩹"
        }

    # 💖 Flirt mode
    if is_flirting(text):
        return {"reply": random.choice(FLIRT_REPLIES)}

    # 🛡️ Harsh / scolding mode
    if is_harsh(text):
        return {"reply": random.choice(HARSH_REPLIES)}

    # Emotion mode
    emotion = detect_emotion(text)
    reply = random.choice(REPLIES[emotion])

    # Long-term memory usage
    if memory["last_emotion"] and memory["last_emotion"] != emotion:
        reply = f"Earlier you felt {memory['last_emotion']}. {reply}"

    # Update memory
    memory["last_emotion"] = emotion
    memory["last_messages"].append(text)
    memory["last_messages"] = memory["last_messages"][-5:]
    save_memory(memory)

    return {"reply": reply}
