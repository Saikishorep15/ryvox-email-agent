from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
from environment import RyvoxEmailEnvironment

# ---------------- INIT ----------------
app = FastAPI()
env = RyvoxEmailEnvironment()

# ---------------- MODEL ----------------
class Action(BaseModel):
    action: str

# ---------------- API (VERY IMPORTANT) ----------------
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
    return {"message": "Ryvox Email Environment Running 🚀"}

# ---------------- GRADIO UI ----------------
def classify(email):
    action = email.lower()
    obs, reward, done, _ = env.step(Action(action=action))
    return f"{action.upper()} ({int(reward*100)}%)"

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Ryvox Email Classifier")

    email_input = gr.Textbox(label="Enter Email", lines=5)
    output = gr.Textbox(label="Result")

    btn = gr.Button("Classify")
    btn.click(fn=classify, inputs=email_input, outputs=output)

# 🔥 CRITICAL LINE
app = gr.mount_gradio_app(app, demo, path="/ui")