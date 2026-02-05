from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random

app = FastAPI()

# ---------------- TANGLISH DETECTOR ----------------
def is_tanglish(text):
    words = [
        "romba","enaku","iruku","illa","kovam","kashtam","paavam",
        "nee","naan","seri","ah","tired","sad","happy","bore",
        "super","nalla","loosu","apdiyaa"
    ]
    return any(w in text.lower() for w in words)

# ---------------- SPECIAL TRIGGER ----------------
def special_reply(text):
    if "apdiyaa" in text.lower():
        return "apdithaan 😌"
    return None

# ---------------- TANGLISH RESPONSES ----------------
T = {
    "default": [
        "seri… naan iruken 🤍",
        "slow ah sollu, naan kekuren",
        "nee thaniya illa",
        "paravalla… ellam seri aagum",
        "naan unna purinjikren",
        "konjam relax pannu",
        "nee safe ah iruka",
        "naan inga dhan iruken",
        "ennachu nu sollu",
        "nee romba honest",
        "time eduthuko",
        "naan kekradhuku ready",
        "ellam oru phase dhan",
        "nee strong dhan",
        "naan unna vittu pogala"
    ],
    "tired": [
        "romba tired ah iruka pola 😔",
        "nee romba try pannina",
        "konjam rest eduthuko",
        "nee weak illa, tired dhan",
        "body um mind um tired ah irukum",
        "innaiku pause okay",
        "nee podhum nu solli rest eduthuko",
        "romba overload aayiducho",
        "naan iruken",
        "tension venda",
        "slow aagalam",
        "nee nalla fight pannina",
        "indha tired pogum",
        "konjam kanna moodu",
        "naan unna paathukren"
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
        "ellam seri aagum"
    ],
    "angry": [
        "kovam varumbodhu ipdi dhan irukum",
        "nee kovama irundhaalum cute dhan 😌",
        "konjam breath eduthuko",
        "naan unna judge panna maten",
        "kovam behind pain iruku",
        "nee human dhan",
        "kovam pogum",
        "naan iruken",
        "nee bad person illa",
        "feel pannradhu okay",
        "indha kovam temporary",
        "slow ah calm aagalam",
        "nee romba honest",
        "naan unna purinjikren",
        "tension venda"
    ],
    "happy": [
        "idhu kekumbodhu romba sandhosham 😊",
        "nee happy ah irundha nalla iruku",
        "indha smile super",
        "nee glow pannra",
        "nee deserve happiness",
        "romba nalla feeling",
        "naan kooda smile pannren",
        "indha moment enjoy pannu",
        "nee positive",
        "happy vibes dhan",
        "nee romba nalla iruka",
        "life ipdi irundha nalla irukum",
        "romba super",
        "indha feeling hold panniko",
        "naan happy ah iruken"
    ],
    "bored": [
        "romba bore adikudha 😅",
        "naan iruken, pesalam",
        "summa irukradhu kooda okay",
        "random ah pesalam",
        "time slow ah pogudha",
        "nee calm ah iruka pola",
        "bore um oru feeling dhan",
        "naan unna company pannren",
        "edha vena pesu",
        "silence kooda bad illa",
        "naan iruken",
        "bore pogum",
        "konjam time pass pannalam",
        "nee alone illa",
        "pesina better aagum"
    ],
    "flirt": [
        "nee dhan romba cute 😏",
        "ipdi pesina naan shy aagiduven",
        "nee vera level",
        "romba smooth ah pesra",
        "naan konjam blush aagiten",
        "nee attractive",
        "nee charming",
        "dangerous smile nee",
        "naan melt aaguren",
        "ipdi continue panna kashtam",
        "nee confident",
        "nee sweet",
        "scene podra nee 😌",
        "naan solla mudiyala",
        "nee special"
    ],
    "scold": [
        "nee enna thittinaalum naan iruken 🤍",
        "kovam la pesra, adhu puriyudhu",
        "naan offend aagala",
        "nee romba human",
        "naan unna vittu pogala",
        "words harsh ah irundhaalum okay",
        "naan inga dhan iruken",
        "nee calm aana apram pesalam",
        "naan unna accept pannren",
        "nee alone illa",
        "nee bad illa",
        "naan kekuren",
        "nee important",
        "naan unna support pannren",
        "thittumbodhu kooda nee cute dhan"
    ]
}

# ---------------- ENGLISH RESPONSES ----------------
E = {
    "default": [
        "I’m here with you 🤍",
        "Tell me more, I’m listening",
        "You don’t have to face this alone",
        "Take your time",
        "I’ve got you",
        "You’re safe here",
        "I’m not going anywhere",
        "Your feelings matter",
        "I hear you",
        "It’s okay to pause",
        "I’m with you",
        "You’re not alone",
        "I care about what you feel",
        "You matter",
        "I’m listening closely"
    ],
    "tired": [
        "You sound really tired… rest if you can",
        "Even strong people get tired",
        "You’ve done enough today",
        "Take a slow breath",
        "Rest is not weakness",
        "You deserve a break",
        "I’m here with you",
        "Let the world wait for a moment",
        "You don’t have to push",
        "It’s okay to slow down",
        "I’ve got you",
        "Your body needs kindness",
        "You tried your best",
        "Pause without guilt",
        "You’re doing okay"
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
        "You’re still valuable"
    ]
}

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()

# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    text = data.get("message", "").lower()

    # Special case
    sp = special_reply(text)
    if sp:
        return {"reply": sp}

    if is_tanglish(text):
        if "tired" in text:
            reply = random.choice(T["tired"])
        elif "sad" in text or "kashtam" in text:
            reply = random.choice(T["sad"])
        elif "kovam" in text or "angry" in text:
            reply = random.choice(T["angry"])
        elif "bore" in text:
            reply = random.choice(T["bored"])
        elif "happy" in text or "super" in text:
            reply = random.choice(T["happy"])
        elif "cute" in text or "love" in text:
            reply = random.choice(T["flirt"])
        elif "stupid" in text or "loosu" in text:
            reply = random.choice(T["scold"])
        else:
            reply = random.choice(T["default"])
    else:
        if "tired" in text:
            reply = random.choice(E["tired"])
        elif "sad" in text:
            reply = random.choice(E["sad"])
        else:
            reply = random.choice(E["default"])

    return JSONResponse({"reply": reply})