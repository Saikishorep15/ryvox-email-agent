import gradio as gr
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

env = RyvoxEmailEnvironment()
history = []


def classify_email(email):
    if not email.strip():
        return "⚠️ Please enter email text", history

    # 🔹 Get task from environment
    obs = env.reset()
    current_state = env.state()

    correct_label = current_state["label"]
    difficulty = current_state["difficulty"]
    email_text = current_state["email_text"]

    # 🔹 Agent decision logic
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

    # 🔹 Output format
    if action_value == "spam":
        result = f"🚨 SPAM ({confidence}%)"
    elif action_value == "important":
        result = f"📌 IMPORTANT ({confidence}%)"
    else:
        result = f"✅ NORMAL ({confidence}%)"

    # 🔥 REQUIRED HISTORY FORMAT
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


# 🎨 PREMIUM CLEAN CSS
css = """
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Center container */
.gradio-container {
    max-width: 1100px !important;
    margin: auto;
}

/* Card look */
#main-box {
    background: #1e293b;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.4);
}

/* Title */
#title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
}

#subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* Input */
textarea {
    background: #0f172a !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: bold;
    height: 45px;
}

/* Result box */
#result-box {
    font-size: 18px;
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
            lines=4
        )

        with gr.Row():
            classify_btn = gr.Button("🔍 Classify Email", variant="primary")
            clear_btn = gr.Button("🧹 Clear")

        output = gr.Textbox(label="Result", elem_id="result-box")

        history_box = gr.JSON(label="📜 History")


        classify_btn.click(classify_email, inputs=email_input, outputs=[output, history_box])
        clear_btn.click(clear_all, outputs=[email_input, output, history_box])


demo.launch(server_name="0.0.0.0", server_port=7860)