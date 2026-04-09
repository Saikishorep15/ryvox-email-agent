
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
            "done": obs.done,
            "task": obs.task  # 🔥 REQUIRED: Tells the grader which task just started
        }
    }

@app.post("/step")
def step(action: Action):
    # Ensure the environment receives the action correctly
    obs, reward, done, _ = env.step(action)

    return {
        "observation": {
            "email_text": obs.email_text,
            "reward": obs.reward,
            "done": obs.done,
            "task": obs.task  # 🔥 REQUIRED: Links this specific reward to a task ID
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

if __name__ == "__main__":
    main()
