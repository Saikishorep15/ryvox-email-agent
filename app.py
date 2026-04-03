from fastapi import FastAPI
import gradio as gr
import random

app = FastAPI()

history = []

spam_words = ["offer", "win", "free", "lottery", "prize"]
important_words = ["urgent", "asap", "meeting", "important"]

def classify_email(text):
    t = text.lower()

    spam = sum(w in t for w in spam_words)
    imp = sum(w in t for w in important_words)

    if spam:
        label, conf, reason = "Spam", random.randint(85,98), "Spam keywords detected"
    elif imp:
        label, conf, reason = "Important", random.randint(75,90), "Urgency detected"
    else:
        label, conf, reason = "Normal", random.randint(70,85), "No strong signals"

    history.append(label)
    if len(history) > 10:
        history.pop(0)

    stats = {
        "Spam": history.count("Spam"),
        "Important": history.count("Important"),
        "Normal": history.count("Normal")
    }

    return f"{label} ({conf}%)\n\n{reason}", stats


@app.post("/classify")
def classify_api(data: dict):
    result, _ = classify_email(data.get("text",""))
    return {"result": result}


# 🔥 MINIMAL PRO CSS (Purple Cow)
css = """
body { background:#0b0b0f; font-family:Inter,sans-serif; }

.container {
    max-width: 900px;
    margin: auto;
    padding-top: 40px;
}

.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 14px;
    padding: 20px;
    backdrop-filter: blur(10px);
}

h1 {
    text-align:center;
    color:#a855f7;
    font-weight:600;
}

textarea {
    background:#050507 !important;
    color:#e5e7eb !important;
    border:1px solid #27272a !important;
}

button {
    background:#7c3aed;
    border-radius:8px !important;
}
button:hover { background:#6d28d9; }
"""

with gr.Blocks(css=css) as demo:

    with gr.Column(elem_classes="container"):

        gr.Markdown("# Ryvox AI")

        with gr.Group(elem_classes="card"):
            text = gr.Textbox(lines=6, placeholder="Paste email...")

            with gr.Row():
                btn = gr.Button("Analyze")
                clr = gr.Button("Clear")

        with gr.Group(elem_classes="card"):
            out = gr.Textbox(label="Result")
            stats = gr.Label(label="Stats")

    btn.click(classify_email, text, [out, stats])
    clr.click(lambda: ("", {}), None, [out, stats])

app = gr.mount_gradio_app(app, demo, path="/")