from fastapi import FastAPI
import gradio as gr
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

# FastAPI
app = FastAPI()
env = RyvoxEmailEnvironment()


# ---------------- API (REQUIRED) ----------------
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


# ---------------- UI (OPTIONAL) ----------------
def classify_email(text):
    action = text.lower()
    obs, reward, done, _ = env.step(RyvoxEmailAction(action=action))
    return f"{action.upper()} ({int(reward*100)}%)"


with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Ryvox Email Classifier")

    input_box = gr.Textbox(label="Enter Email")
    output_box = gr.Textbox(label="Result")

    btn = gr.Button("Classify")

    btn.click(fn=classify_email, inputs=input_box, outputs=output_box)


# 🔥 THIS IS KEY
app = gr.mount_gradio_app(app, demo, path="/")