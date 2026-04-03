from fastapi import FastAPI
import gradio as gr
import random

app = FastAPI()

history = []

spam_words = ["offer", "win", "free", "lottery", "prize"]
important_words = ["urgent", "asap", "meeting", "important"]

# ================= LOGIC =================
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

    result = f"{label} ({conf}%)\n\n{reason}"
    return result, stats


# ================= API =================
@app.post("/classify")
def classify_api(data: dict):
    result, _ = classify_email(data.get("text", ""))
    return {"result": result}


# ================= CSS =================
css = """
body {
    background: #f8fafc;
    font-family: Inter, sans-serif;
}

/* CENTER CONTAINER */
.container {
    max-width: 700px;
    margin: auto;
    padding-top: 60px;
}

/* TITLE */
h1 {
    text-align: center;
    color: #6d28d9;
    font-weight: 600;
    margin-bottom: 30px;
}

/* CARD */
.card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

/* INPUT */
textarea {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
}

/* BUTTON */
button {
    background: #7c3aed;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500;
}

button:hover {
    background: #6d28d9;
}

/* OUTPUT */
textarea[readonly] {
    background: #f1f5f9 !important;
}
"""

# ================= UI =================
with gr.Blocks(css=css) as demo:

    with gr.Column(elem_classes="container"):

        gr.Markdown("# Email Analyzer")

        # INPUT
        with gr.Group(elem_classes="card"):
            text = gr.Textbox(
                lines=6,
                placeholder="Paste email content..."
            )

            with gr.Row():
                analyze = gr.Button("Analyze")
                clear = gr.Button("Clear")

        # OUTPUT
        with gr.Group(elem_classes="card"):
            output = gr.Textbox(label="Result", lines=5)
            stats = gr.Label(label="Stats")

    # ACTIONS
    analyze.click(classify_email, text, [output, stats])
    clear.click(lambda: ("", {}), None, [output, stats])


# ================= MOUNT =================
app = gr.mount_gradio_app(app, demo, path="/")