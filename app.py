import gradio as gr
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction
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
env = RyvoxEmailEnvironment()
history = []


def classify_email(email):
    if not email.strip():
        return "⚠️ Please enter email text", history

    # Use environment
    obs = env.reset()
    state = env.state()

    email_text = state["email_text"]
    correct_label = state["label"]
    difficulty = state["difficulty"]

    email_lower = email_text.lower()

    if "win" in email_lower or "offer" in email_lower or "money" in email_lower:
        action_value = "spam"
    elif "meeting" in email_lower or "project" in email_lower or "discuss" in email_lower:
        action_value = "important"
    else:
        action_value = "normal"

    action = RyvoxEmailAction(action=action_value)
    obs, reward, done, _ = env.step(action)

    confidence = int(reward * 100)

    if action_value == "spam":
        result = f"🚨 SPAM ({confidence}%)"
    elif action_value == "important":
        result = f"📌 IMPORTANT ({confidence}%)"
    else:
        result = f"✅ NORMAL ({confidence}%)"

    # RL history
    history.append({
        "email": email_text,
        "action": action_value,
        "correct_label": correct_label,
        "reward": reward,
        "difficulty": difficulty
    })

    return result, history


def clear_all():
    history.clear()
    return "", "", []


# 🔥 ONLY EXPANDED SIZE (NO DESIGN CHANGE)
css = """
body {
    background: #0f172a;
}

/* 🔥 EXPAND FULL WIDTH */
.gradio-container {
    max-width: 1400px !important;
    margin: auto;
}

/* 🔥 BIGGER BOX */
#main-box {
    background: #1e293b;
    padding: 50px;
    border-radius: 15px;
    width: 100%;
}

/* Title */
#title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: white;
    margin-bottom: 15px;
}

/* Subtitle */
#subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Input */
textarea {
    background: #0f172a !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 16px;
}

/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: bold;
    height: 50px;
    font-size: 16px;
}

/* Result */
#result-box {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}
"""


with gr.Blocks(css=css) as demo:

    with gr.Column(elem_id="main-box"):

        gr.Markdown("<div id='title'>🚀 Ryvox AI Email Classifier</div>")
        gr.Markdown("<div id='subtitle'>Classify emails as Spam, Important, or Normal using AI logic</div>")

        email_input = gr.Textbox(
            label="Enter Email Content",
            placeholder="Paste email content here...",
            lines=5
        )

        with gr.Row():
            classify_btn = gr.Button("🔍 Classify Email", variant="primary")
            clear_btn = gr.Button("🧹 Clear")

        output = gr.Textbox(label="Result", elem_id="result-box")

        gr.Markdown("### 📊 Evaluation History (Agent Performance)")
        history_box = gr.JSON(label="History")

        classify_btn.click(classify_email, inputs=email_input, outputs=[output, history_box])
        clear_btn.click(clear_all, outputs=[email_input, output, history_box])


demo.launch(server_name="0.0.0.0", server_port=7860)