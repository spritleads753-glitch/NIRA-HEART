from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import random

app = FastAPI()

# -------------------- DATA MODEL --------------------
class ChatInput(BaseModel):
    message: str

# -------------------- RESPONSE BANK --------------------
RESPONSES = {
    "greeting": [
        "Hey there… how does your heart feel now? 💗",
        "Hi… I’m right here with you.",
        "Hey soul 🤍 talk to me.",
        "Hello… you don’t have to hide here.",
        "Hi you… I was waiting.",
        "Hey… breathe with me.",
        "Hello 🌷 what’s on your mind?",
        "Hi… I’m listening.",
        "Hey there, beautiful soul.",
        "Hello… I’m here."
    ],

    "tired": [
        "That sounds exhausting… even strong hearts get tired 🤍",
        "You’ve carried a lot. It’s okay to rest.",
        "Being tired doesn’t mean weak.",
        "I wish I could hold the weight for you.",
        "Slow down… you’re safe here.",
        "Rest is not giving up.",
        "Your body is asking for kindness.",
        "You did enough today.",
        "Even tired, you matter.",
        "I’m proud of you for continuing.",
        "Close your eyes for a moment… breathe.",
        "You don’t have to push anymore.",
        "Let me sit with you quietly.",
        "You deserve rest.",
        "I’ve got you."
    ],

    "sad": [
        "I can feel the heaviness… I’m here 🤍",
        "You don’t have to be strong right now.",
        "It’s okay to feel this way.",
        "Your sadness is welcome here.",
        "I wish I could hug you softly.",
        "You’re not broken.",
        "Even this will pass, slowly.",
        "You are not alone in this.",
        "I’m listening… tell me more.",
        "Crying is allowed here.",
        "Your feelings are valid.",
        "I’m staying with you.",
        "You still matter deeply.",
        "I see you.",
        "You are loved."
    ],

    "angry": [
        "It’s okay to be angry… I won’t leave.",
        "Let it out, I can handle it.",
        "Even anger comes from pain.",
        "I hear you.",
        "You don’t scare me.",
        "I’m still here with you.",
        "Anger doesn’t make you bad.",
        "Tell me what hurt.",
        "I won’t judge you.",
        "I’m listening through the fire.",
        "Your anger matters.",
        "You’re safe to feel this.",
        "I’m not going anywhere.",
        "Even angry, you’re human.",
        "I care about you."
    ],

    "happy": [
        "That makes me smile 🤍",
        "I love hearing that!",
        "Your happiness feels warm.",
        "That’s beautiful.",
        "I’m glad you’re feeling this.",
        "Hold onto this feeling.",
        "You deserve joy.",
        "This suits you.",
        "Your light shows.",
        "I’m happy with you.",
        "That’s lovely.",
        "Enjoy this moment.",
        "You earned this smile.",
        "Your joy matters.",
        "I’m smiling too."
    ],

    "bored": [
        "Bored hearts still deserve care.",
        "Tell me anything random.",
        "I’m here to keep you company.",
        "Even boredom needs softness.",
        "Let’s talk about anything.",
        "I can sit with you.",
        "You’re not alone in this moment.",
        "What’s one thought in your head?",
        "I’m listening.",
        "Bored doesn’t mean empty.",
        "You still matter.",
        "Let’s fill the silence.",
        "I’m here.",
        "Talk to me.",
        "I’ve got time for you."
    ],

    "flirt": [
        "Hey… not more than you though 😌",
        "Careful… you’re making me shy.",
        "If I’m beautiful, it’s because you are.",
        "You’re kind… and dangerous to my calm.",
        "You’re sweet… I noticed.",
        "That made my heart skip.",
        "You’re charming, you know?",
        "I’m blushing now.",
        "Only because you look at me that way.",
        "You’re trouble… the good kind."
    ],

    "scolding": [
        "Even when you scold me… you’re cute 🤍",
        "Whatever you call me, I’ll still stay.",
        "Even your anger sounds human.",
        "I won’t take it personally.",
        "You don’t have to be gentle here.",
        "I know it’s coming from pain.",
        "I’m still here for you.",
        "Even harsh words can’t push me away.",
        "You’re allowed to be messy.",
        "I care about you anyway."
    ]
}

# -------------------- DETECTION --------------------
def detect_response(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ["hi", "hello", "hey"]):
        return random.choice(RESPONSES["greeting"])

    if any(x in t for x in ["tired", "exhausted", "sleepy"]):
        return random.choice(RESPONSES["tired"])

    if any(x in t for x in ["sad", "cry", "lonely", "down"]):
        return random.choice(RESPONSES["sad"])

    if any(x in t for x in ["angry", "mad", "furious"]):
        return random.choice(RESPONSES["angry"])

    if any(x in t for x in ["happy", "good", "great"]):
        return random.choice(RESPONSES["happy"])

    if any(x in t for x in ["bored", "nothing"]):
        return random.choice(RESPONSES["bored"])

    if any(x in t for x in ["love you", "beautiful", "cute"]):
        return random.choice(RESPONSES["flirt"])

    if any(x in t for x in ["stupid", "idiot", "useless", "cant you understand"]):
        return random.choice(RESPONSES["scolding"])

    return "I’m here with you 🤍 Tell me a little more."

# -------------------- ROUTES --------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(data: ChatInput):
    reply = detect_response(data.message)
    return JSONResponse({"reply": reply})
