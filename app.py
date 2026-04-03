import sys
import os
from fastapi import FastAPI

# --- HACKATHON PATH FIX ---
# This ensures Python looks in the current folder for 'environment' and 'models'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now we can safely import your custom modules
try:
    from environment import RyvoxEmailEnvironment
    from models import RyvoxEmailAction, RyvoxEmailObservation
except ImportError as e:
    print(f"CRITICAL ERROR: Could not find environment.py or models.py. Error: {e}")
    sys.exit(1)

# --- APP INITIALIZATION ---
app = FastAPI(title="Ryvox Email RL Environment")

# Initialize the RL environment logic
env = RyvoxEmailEnvironment()

@app.get("/")
async def root():
    return {"status": "Online", "message": "Ryvox Email Environment is running!"}

@app.post("/reset")
async def reset():
    """
    Resets the environment to a random starting email.
    Returns: RyvoxEmailObservation
    """
    observation = env.reset()
    return {"observation": observation}

@app.post("/step")
async def step(action: RyvoxEmailAction):
    """
    Takes an action ('spam', 'important', 'normal') and returns feedback.
    Returns: observation, reward, done
    """
    observation, reward, done, info = env.step(action)
    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)