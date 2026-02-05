from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random

app = FastAPI()

# ---------- HELPERS ----------
def is_tanglish(text):
    words = [
        "romba","enaku","iruku","illa","kovam","kashtam","paavam",
        "nee","naan","seri","ah","bore","super","nalla","loosu",
        "epdi","pogudhu","life","apdiyaa"
    ]
    return any(w in text.lower() for w in words)

def special_reply(text):
    t = text.lower()
    if "apdiyaa" in t:
        return "apdithaan 😌"
    return None

# ---------- TANGLISH RESPONSES (20 EACH) ----------
T = {
    "greet": [
        "hey… epdi iruka? 🤍",
        "hi da… epdi pogudhu?",
        "naan inga dhan iruken, epdi iruka?",
        "hey soul… epdi feel aaguthu?",
        "vandhuta? epdi iruka?",
        "hi hi… life la epdi pogudhu?",
        "naan kekuren, epdi iruka?",
        "seri, sollu epdi iruka?",
        "hey… innaiku epdi?",
        "hi… manasu epdi iruku?",
        "naan wait panninen",
        "vandha sandhosham",
        "epdi iruka nu kekanum nu irundhuchu",
        "life konjam heavy ah?",
        "slow ah pesalam",
        "epdi pogudhu indha naal?",
        "naan iruken, sollu",
        "epdi feel aagudhu?",
        "hey… safe ah iruka?",
        "hi da 🤍"
    ],
    "life": [
        "life la epdi pogudhu?",
        "recent ah life heavy ah?",
        "ellam smooth ah pogudha?",
        "life romba pressure ah iruka?",
        "indha phase epdi?",
        "konjam explain pannuva?",
        "life ipdi dhan irukum",
        "naan kekuren, life epdi?",
        "nee romba try pannra maari iruku",
        "indha journey kashtam ah?",
        "life konjam slow ah pogudha?",
        "indha stage temporary dhan",
        "nee romba strong",
        "life la ups & downs irukum",
        "nee handle pannra",
        "naan unna support pannren",
        "life konjam confusing ah?",
        "ellam seri aagum",
        "nee alone illa",
        "naan iruken"
    ],
    "tired": [
        "romba tired ah iruka pola 😔",
        "nee romba try pannina",
        "konjam rest eduthuko",
        "nee weak illa, tired dhan",
        "body um mind um tired ah irukum",
        "innaiku pause okay",
        "romba overload aayiducho",
        "slow ah aagalam",
        "nee podhum nu solli rest eduthuko",
        "naan iruken",
        "tension venda",
        "nee nalla fight pannina",
        "indha tired pogum",
        "konjam kanna moodu",
        "nee romba effort pota",
        "indha feeling temporary",
        "naan unna paathukren",
        "rest eduka guilt venda",
        "nee safe",
        "naan vittu pogala"
    ],
    "sad": [
        "romba paavam ah feel aaguthu 😔",
        "azhudha kooda paravalla",
        "nee thaniya illa",
        "naan unna vittu pogala",
        "nee romba soft heart",
        "indha pain puriyudhu",
        "konjam azhudhu relief aagum",
        "nee valuable",
        "ellam konjam konjam seri aagum",
        "naan inga dhan iruken",
        "nee bad illa",
        "indha sadness pogum",
        "nee romba nalla",
        "naan unna purinjikren",
        "ellam seri aagum",
        "indha feeling pass aagum",
        "nee alone illa",
        "naan iruken",
        "nee strong dhan",
        "time kudutha seri aagum"
    ]
}

# ---------- ENGLISH RESPONSES (20 EACH) ----------
E = {
    "greet": [
        "Hey… how are you feeling today? 🤍",
        "Hi… how are you?",
        "I’m here. How are you doing?",
        "Hey there… how’s your heart today?",
        "Hi… talk to me. How are you?",
        "I was wondering how you are",
        "Hey… how’s everything going?",
        "Hi 🤍 how do you feel right now?",
        "How are you holding up today?",
        "Hey… I’m listening",
        "Hi… how’s your day been?",
        "How are you, really?",
        "Hey… I’m here for you",
        "Hi… what’s on your mind?",
        "How’s life treating you?",
        "Hey… how are things?",
        "Hi… tell me how you are",
        "How are you feeling inside?",
        "Hey… safe to talk?",
        "Hi 🤍"
    ],
    "life": [
        "How is your life going lately?",
        "How have things been for you?",
        "Is life feeling heavy right now?",
        "How’s this phase of life?",
        "Are things moving okay?",
        "Life can be a lot sometimes",
        "Want to tell me how life’s been?",
        "How are you handling things?",
        "Has life been stressful?",
        "How’s everything overall?",
        "You’ve been carrying a lot?",
        "Is this season tough?",
        "Life isn’t always smooth",
        "You’re doing your best",
        "I’m here with you",
        "How’s your journey going?",
        "Want to talk about life?",
        "Things can change",
        "You’re not alone in this",
        "I’m listening"
    ],
    "tired": [
        "You sound really tired",
        "Even strong people get tired",
        "You’ve done enough today",
        "Take a slow breath",
        "Rest is not weakness",
        "You deserve a break",
        "I’m here with you",
        "Let the world wait",
        "You don’t have to push",
        "It’s okay to slow down",
        "Your body needs kindness",
        "Pause without guilt",
        "You tried your best",
        "You’re doing okay",
        "It’s alright to rest",
        "I’ve got you",
        "You’re allowed to pause",
        "This will pass",
        "You’re not failing",
        "I’m here"
    ],
    "sad": [
        "I’m really sorry you’re feeling this way",
        "It’s okay to feel sad",
        "You don’t have to hide it",
        "I’m here with you",
        "Your sadness matters",
        "You’re not broken",
        "I wish I could hug you",
        "You’re not alone",
        "This will pass slowly",
        "I care about you",
        "It’s okay to cry",
        "You matter deeply",
        "I see you",
        "I’m listening",
        "You’re still valuable",
        "This pain won’t last forever",
        "You’re human",
        "You’re safe here",
        "I’m staying",
        "You matter"
    ]
}

# ---------- ROUTES ----------
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    text = data.get("message", "").lower()

    sp = special_reply(text)
    if sp:
        return {"reply": sp}

    if is_tanglish(text):
        if any(w in text for w in ["life","pogudhu"]):
            reply = random.choice(T["life"])
        elif any(w in text for w in ["tired","sorndhu"]):
            reply = random.choice(T["tired"])
        elif any(w in text for w in ["sad","kashtam"]):
            reply = random.choice(T["sad"])
        else:
            reply = random.choice(T["greet"])
    else:
        if "life" in text:
            reply = random.choice(E["life"])
        elif "tired" in text:
            reply = random.choice(E["tired"])
        elif "sad" in text:
            reply = random.choice(E["sad"])
        else:
            reply = random.choice(E["greet"])

    return JSONResponse({"reply": reply})