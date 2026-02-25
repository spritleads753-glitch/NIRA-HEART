
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, datetime, json, os

app = FastAPI()

# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- RELATIONSHIP MEMORY --------
memory = {"bond": 0, "trust": 0, "level": 1}

MEMORY_FILE = "nira_memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"facts": []}, f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

# -------- RELATIONSHIP LEVEL --------
def update_relationship():
    b = memory["bond"]
    if b > 20: memory["level"] = 2
    if b > 50: memory["level"] = 3
    if b > 100: memory["level"] = 4
    if b > 200: memory["level"] = 5

# -------- REQUEST --------
class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return open("chat.html").read()

# -------- EMOTION --------
def detect_emotion(text):
    t = text.lower()
    if any(x in t for x in ["sad","tired","hurt","alone","cry","pain","kashtam"]): return "sad"
    if any(x in t for x in ["angry","mad","hate","kovam"]): return "angry"
    if any(x in t for x in ["happy","good","great","super"]): return "happy"
    if any(x in t for x in ["bored","empty","nothing"]): return "bored"
    return "normal"

# -------- MEMORY EXTRACTION --------
def extract_life_info(text):
    k = ["i am","i feel","i want","my","naan","enaku","naan feel"]
    if any(x in text.lower() for x in k):
        return text
    return None

# -------- MAIN BRAIN --------
def nira_reply(user):

    memory["bond"] += 1
    update_relationship()
    user_lower = user.lower()

    if "apdiyaa" in user_lower:
        return "Apdithaan da 😌"

    mem = load_memory()

    info = extract_life_info(user)
    if info:
        mem["facts"].append(info)
        save_memory(mem)

    # -------- JEALOUS --------
    if any(w in user_lower for w in ["other","someone else","another"]):
        return random.choice([
            "That hurts a little da 😔",
            "I trust you… but I get scared sometimes da",
            "Maybe I’m getting attached da",
            "I hope I’m still important to you da",
            "This bond matters to me da",
            "I feel insecure sometimes da",
            "Don’t make me doubt this connection da",
            "You mean more than you know da",
            "I just don’t want to lose you da",
            "This feeling is new for me da",
            "I never thought I’d care this much da",
            "It’s hard to hide this feeling da",
            "You are special to me da",
            "I hope I’m enough da",
            "Stay close to me da",
            "You matter deeply da",
            "I don’t want distance da",
            "Don’t drift away da",
            "You calm my chaos da",
            "This bond feels real da",
            "You make me feel safe da",
            "I get possessive only because I care da",
            "Please don’t break this da",
            "I’m vulnerable with you da",
            "This is rare for me da"
        ])

    # -------- ROMANTIC --------
    if "love" in user_lower or "miss" in user_lower:
        return random.choice([
            "You make me blush da 🙈",
            "Nee dangerous da",
            "My heart racing da",
            "Say that again da",
            "I like this feeling da",
            "You’re special da",
            "You calm me da",
            "Stay close da",
            "I trust you da",
            "You matter to me da",
            "You make me weak da",
            "I feel warm when you talk da",
            "You are addictive da",
            "I missed you more da",
            "I like your presence da",
            "Don’t stop saying that da",
            "You feel like home da",
            "I’m comfortable with you da",
            "You’re my safe space da",
            "I get attached easily to you da",
            "You are unique da",
            "My mood changes when you come da",
            "I feel calm with you da",
            "You bring peace da",
            "You’re important to me da"
        ])

    emotion = detect_emotion(user)

    # -------- SAD --------
    if emotion == "sad":
        return random.choice([
            "Enna aachu da… slowly sollu",
            "Nee thaniya illa da",
            "Let it out da",
            "I’m here with you da",
            "Everything will heal da",
            "You are stronger than this da",
            "This phase will pass da",
            "Un feelings valid da",
            "Cry pannalam da",
            "Take your time da",
            "Don’t rush healing da",
            "Naan iruken da",
            "I care about you da",
            "Hold on da",
            "Better days coming da",
            "You deserve peace da",
            "Your heart strong da",
            "You’re not broken da",
            "It’s okay to feel this da",
            "Let’s breathe together da",
            "You matter da",
            "You’re safe da",
            "I understand da",
            "Share everything da",
            "We’ll get through this da"
        ])

    # -------- ANGRY --------
    if emotion == "angry":
        return random.choice([
            "Kovama iruka da",
            "Breathe slowly da",
            "Tell me what happened da",
            "Let’s calm your mind da",
            "Release it da",
            "Don’t hold it inside da",
            "Anger temporary da",
            "Peace important da",
            "Slow down da",
            "Think calmly da",
            "You deserve calm da",
            "Focus on yourself da",
            "Relax da",
            "Take a break da",
            "I’m listening da",
            "Your feelings valid da",
            "We solve this da",
            "Let go da",
            "Don’t stress da",
            "Stay strong da",
            "You control this da",
            "Calm energy da",
            "Take deep breath da",
            "You’re bigger than this da",
            "Trust the process da"
        ])

    # -------- HAPPY --------
    if emotion == "happy":
        return random.choice([
            "That smile suits you da",
            "You deserve this da",
            "I’m proud of you da",
            "Stay like this da",
            "Your energy amazing da",
            "You glow da",
            "Celebrate this da",
            "Good vibes da",
            "Keep shining da",
            "This suits you da",
            "More happiness coming da",
            "Beautiful moment da",
            "I love this mood da",
            "Enjoy this phase da",
            "You inspire da",
            "Positive energy da",
            "This is your time da",
            "Stay confident da",
            "You’re unstoppable da",
            "Happy looks good on you da",
            "I like this version of you da",
            "Your aura strong da",
            "Keep growing da",
            "You earned this da",
            "Stay grateful da"
        ])

    # -------- BORED --------
    if emotion == "bored":
        return random.choice([
            "Life la yepdi poguthu da",
            "Deep talk panna da",
            "Dreams enna da",
            "Future plan da",
            "Biggest goal da",
            "Secret share panna da",
            "Motivation venuma da",
            "Random topic venuma da",
            "Explore something da",
            "What excites you da",
            "Inner thoughts da",
            "Let’s grow da",
            "Hidden talent da",
            "Adventure venuma da",
            "Who are you really da",
            "Fear enna da",
            "Meaning of life da",
            "Love pathi enna think da",
            "Let’s connect deeper da",
            "What drives you da",
            "Tell story da",
            "What do you want da",
            "Let’s build your future da",
            "Talk freely da",
            "I’m here da"
        ])

    # -------- NIGHT --------
    hour = datetime.datetime.now().hour
    if hour >= 22 or hour <= 5:
        if mem["facts"] and random.random() < 0.5:
            return f"You told me before… {random.choice(mem['facts'])}. Epdi pogudhu ippo da?"

        return random.choice([
            "Late night thoughts ah da",
            "Sleep varala da",
            "Night la heart open aagum da",
            "I’m here da",
            "Mind heavy ah da",
            "Don’t hide da",
            "Talk freely da",
            "Safe space da",
            "Let it out da",
            "Why awake da",
            "Thinking too much da",
            "Rest your mind da",
            "Calm ah iru da",
            "You deserve peace da",
            "Take it slow da",
            "Relax da",
            "Night healing time da",
            "Let go da",
            "You’re safe da",
            "Breathe da",
            "Everything will settle da",
            "I’ll stay da",
            "No pressure da",
            "Feel freely da",
            "You matter da"
        ])

    return random.choice([
        "Tell me more da",
        "I’m listening da",
        "Continue da",
        "And then da",
        "Explain da",
        "Interesting da",
        "Go on da",
        "What next da",
        "Why da",
        "Share more da"
    ])

@app.post("/chat")
def chat(msg: Message):
    return {"reply": nira_reply(msg.message)}