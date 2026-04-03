from fastapi import FastAPI
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

app = FastAPI()
env = RyvoxEmailEnvironment()

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": {
            "email_text": obs.email_text,
            "reward": obs.reward,
            "done": obs.done
        }
    }

@app.post("/step")
def step(action: RyvoxEmailAction):
    obs, reward, done, _ = env.step(action)

    return {
        "observation": {
            "email_text": obs.email_text,
            "reward": obs.reward,
            "done": obs.done
        },
        "reward": reward,
        "done": done
    }

@app.get("/")
def root():
    return {"message": "Ryvox Email Environment Running 🚀"}