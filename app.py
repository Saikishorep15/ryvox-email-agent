import gradio as gr
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

env = RyvoxEmailEnvironment()
history = []


def classify_email(email):
    if not email.strip():
        return "⚠️ Please enter email text", history

    email_lower = email.lower()

    # Simple logic
    if "win" in email_lower or "offer" in email_lower or "money" in email_lower:
        action_value = "spam"
    elif "meeting" in email_lower or "project" in email_lower or "discuss" in email_lower:
        action_value = "important"
    else:
        action_value = "normal"

    action = RyvoxEmailAction(action=action_value)
    obs, reward, done, _ = env.step(action)

    confidence = int(reward * 100)

    result = f"{action_value.upper()} ({confidence}%)"

    history.append({
        "email": email,
        "result": result
    })

    return result, history


def clear_all():
    history.clear()
    return "", "", []


# 🎨 SIMPLE PROFESSIONAL CSS
css = """
body {
    background: #0f172a;
}

.gradio-container {
    max-width: 900px;
    margin: auto;
}

textarea, input {
    background: #1e293b !important;
    color: white !important;
    border-radius: 8px !important;
}

button {
    border-radius: 8px !important;
    font-weight: 600;
}

button:hover {
    opacity: 0.9;
}

#title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
}
"""


with gr.Blocks(css=css) as demo:

    gr.Markdown("<div id='title'>Ryvox Email Classifier</div>")

    email_input = gr.Textbox(
        label="Email Input",
        placeholder="Paste email content here..."
    )

    with gr.Row():
        classify_btn = gr.Button("Classify", variant="primary")
        clear_btn = gr.Button("Clear")

    output = gr.Textbox(label="Result")
    history_box = gr.JSON(label="History")

    classify_btn.click(classify_email, inputs=email_input, outputs=[output, history_box])
    clear_btn.click(clear_all, outputs=[email_input, output, history_box])


demo.launch(server_name="0.0.0.0", server_port=7860)