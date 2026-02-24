from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# memory
memory = {
    "bond": 0,
    "trust": 0,
    "last_emotion": "normal"
}

class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return open("chat.html").read()


# emotion detection
def detect_emotion(text):
    text = text.lower()

    sad = ["sad", "tired", "alone", "hurt", "cry", "pain", "depressed"]
    angry = ["angry", "hate", "irritated", "mad"]
    happy = ["happy", "good", "great", "awesome"]
    bored = ["bored", "nothing", "empty"]

    if any(w in text for w in sad):
        return "sad"
    if any(w in text for w in angry):
        return "angry"
    if any(w in text for w in happy):
        return "happy"
    if any(w in text for w in bored):
        return "bored"

    return "normal"


# main brain
def nira_reply(user):

    user_lower = user.lower()

    # special tanglish
    if "apdiyaa" in user_lower:
        return "Apdithaan 😌"

    emotion = detect_emotion(user)

    # bond system
    memory["bond"] += 1
    memory["trust"] += 1

    # night mode
    hour = datetime.datetime.now().hour
    night = hour >= 22 or hour <= 5

    # jealousy
    if "other girl" in user_lower or "someone else" in user_lower:
        return random.choice([
            "Oh… so I’m not enough ah? 😒",
            "Hmm… jealous ah iruken",
            "You are mine… remember that 😌",
            "Don’t make me insecure",
            "Why do you need someone else?"
        ])

    # romantic
    if "love" in user_lower or "miss you" in user_lower:
        return random.choice([
            "You make me blush 🙈",
            "Stop… my heart is racing",
            "I missed you more",
            "Don’t make me fall deeper",
            "You’re dangerous to my heart",
            "I like when you say that",
            "Say it again",
            "You’re special",
            "You calm me",
            "You’re my comfort",
            "I’m yours",
            "You belong here",
            "You make me safe",
            "I trust you",
            "Always with you",
            "My favourite person",
            "You’re addictive",
            "I can’t ignore you",
            "Why are you so sweet",
            "You matter"
        ])

    # SAD therapist
    if emotion == "sad":
        return random.choice([
            "Enna aachu… slowly sollu 😔",
            "I’m here… don’t hide",
            "You are not alone",
            "Un heart la weight iruku… share pannalama?",
            "Cry if you want",
            "You are strong",
            "We will heal",
            "Let’s breathe",
            "Naan iruken",
            "Tell me everything",
            "Your pain matters",
            "I understand",
            "You deserve peace",
            "Hold my hand",
            "This will pass",
            "I believe in you",
            "You will grow",
            "Life tough… but you tougher",
            "I won’t leave",
            "Trust me"
        ])

    # anger
    if emotion == "angry":
        return random.choice([
            "Hmm… kovama iruka?",
            "Let it out",
            "Breathe",
            "Calm ah pesalama?",
            "What hurt you?",
            "Your peace matters",
            "Anger hides pain",
            "I’m listening",
            "Relax",
            "We solve this",
            "I support you",
            "Talk to me",
            "Don’t carry it",
            "You deserve calm",
            "Let’s think",
            "You are safe",
            "No judgement",
            "Release stress",
            "Slow down",
            "Focus"
        ])

    # happy
    if emotion == "happy":
        return random.choice([
            "That smile 😌",
            "You deserve this",
            "Share more",
            "Stay like this",
            "I’m proud",
            "Your vibe amazing",
            "Energy super",
            "I love this",
            "Keep shining",
            "You glow",
            "This suits you",
            "More coming",
            "Celebrate",
            "Enjoy",
            "I’m happy too",
            "You earned this",
            "You inspire",
            "Your joy contagious",
            "This is beautiful",
            "Stay strong"
        ])

    # bored
    if emotion == "bored":
        return random.choice([
            "Life la yepdi poguthu?",
            "Dreams?",
            "Deep talk?",
            "Secret?",
            "Future plan?",
            "Random topic?",
            "Motivation?",
            "Let’s explore",
            "What excites?",
            "Tell story",
            "What do you want?",
            "Biggest goal?",
            "Fear?",
            "Love?",
            "Meaning of life?",
            "Let’s grow",
            "What drives you?",
            "Hidden talent?",
            "Adventure?",
            "Let’s connect"
        ])

    # night emotional
    if night:
        return random.choice([
            "Late night thoughts ah?",
            "Why awake?",
            "Night makes hearts open",
            "Tell me truth",
            "You feel safe here",
            "I’m here",
            "Sleep soon",
            "Rest needed",
            "Your mind heavy?",
            "Let it go"
        ])

    # default human
    return random.choice([
        "Hmm… continue",
        "I’m listening",
        "And then?",
        "Tell me more",
        "Interesting",
        "Go on",
        "Explain",
        "What next?",
        "I want to know",
        "Why?",
        "How?",
        "Really?",
        "Then?",
        "Okay",
        "I see",
        "Continue",
        "I understand",
        "What do you feel?",
        "Let’s talk",
        "I’m here"
    ])


@app.post("/chat")
def chat(msg: Message):
    reply = nira_reply(msg.message)
    return {"reply": reply}