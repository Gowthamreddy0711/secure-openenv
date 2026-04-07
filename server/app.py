from fastapi import FastAPI
from .environment import SecureEnvironment
from tasks import easy_task, medium_task, hard_task

app = FastAPI(title="Secure OpenEnv API")

env = SecureEnvironment()


# ✅ ROOT
@app.get("/")
def home():
    return {"message": "🚀 Secure OpenEnv server is running"}


# ✅ Health
@app.get("/health")
def health():
    return {"status": "healthy"}


# ✅ Reset
@app.post("/reset")
def reset():
    return env.reset()


# ✅ Step
@app.post("/step")
def step(action: dict):
    return env.step(action)


# ✅ State
@app.get("/state")
def state():
    return env.state


# ✅ Tasks
@app.get("/tasks")
def tasks():
    state = env._obs(0, False)

    return {
        "easy": easy_task(state),
        "medium": medium_task(state),
        "hard": hard_task(state)
    }


# 🔥 NEW: FINAL SCORE SYSTEM
@app.get("/score")
def score():
    state = env.state

    # Stability decreases with time and load
stability = max(0, 100 - state["step_count"] * 2)

# Security depends on breaches
security = max(0, 100 - state["breaches"] * 30)

# Normalize to 0–1
final_score = (stability * 0.4 + security * 0.6) / 100
   

    return {
        "final_score": round(final_score, 2),
        "stability": stability,
        "security": security
    }
