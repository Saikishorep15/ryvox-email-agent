from fastapi import FastAPI
from pydantic import BaseModel
from environment import RyvoxEmailEnvironment

app = FastAPI()

env = RyvoxEmailEnvironment()


class Action(BaseModel):
    action: str


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
def step(action: Action):
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
    return {"message": "Running 🚀"}


# 🔥 IMPORTANT FIX
def main():
    return app