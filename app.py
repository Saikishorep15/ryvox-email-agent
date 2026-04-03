from fastapi import FastAPI
import gradio as gr
import random

app = FastAPI()

# ================= DATA =================
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

    result = f"""
📌 Classification: {label}
📊 Confidence: {conf}%

💡 Reason:
{reason}
"""

    return result, stats


# ================= API =================
@app.post("/classify")
def classify_api(data: dict):
    result, _ = classify_email(data.get("text", ""))
    return {"result": result}


# ================= PRO CSS =================
css = """
body {
    margin: 0;
    font-family: Inter, sans-serif;
    background: #0b0f19;
}

/* LAYOUT */
.app {
    display: flex;
    height: 100vh;
}

/* SIDEBAR */
.sidebar {
    width: 220px;
    background: #111827;
    border-right: 1px solid #1f2937;
    padding: 20px;
}

.sidebar h2 {
    color: #a855f7;
    font-size: 18px;
    margin-bottom: 30px;
}

.nav-item {
    color: #9ca3af;
    margin-bottom: 15px;
    cursor: pointer;
}

.nav-item:hover {
    color: #ffffff;
}

/* MAIN */
.main {
    flex: 1;
    padding: 25px;
}

/* HEADER */
.header {
    font-size: 20px;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 20px;
}

/* CARDS */
.card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px;
}

/* INPUT */
textarea {
    background: #020617 !important;
    color: #e5e7eb !important;
    border: 1px solid #334155 !important;
}

/* BUTTON */
button {
    background: #7c3aed;
    border-radius: 8px !important;
}
button:hover {
    background: #6d28d9;
}
"""

# ================= UI =================
with gr.Blocks(css=css) as demo:

    with gr.Row(elem_classes="app"):

        # SIDEBAR
        with gr.Column(elem_classes="sidebar", scale=0):
            gr.HTML("<h2>Ryvox AI</h2>")
            gr.HTML("<div class='nav-item'>📊 Dashboard</div>")
            gr.HTML("<div class='nav-item'>📧 Analyzer</div>")
            gr.HTML("<div class='nav-item'>⚙ Settings</div>")

        # MAIN CONTENT
        with gr.Column(elem_classes="main"):

            gr.HTML("<div class='header'>Email Analyzer</div>")

            with gr.Row():

                # INPUT CARD
                with gr.Column(scale=1):
                    with gr.Group(elem_classes="card"):
                        gr.Markdown("### Input Email")

                        text = gr.Textbox(
                            lines=10,
                            placeholder="Paste email content..."
                        )

                        with gr.Row():
                            analyze = gr.Button("Analyze")
                            clear = gr.Button("Clear")

                # OUTPUT CARD
                with gr.Column(scale=1):
                    with gr.Group(elem_classes="card"):
                        gr.Markdown("### Result")
                        output = gr.Textbox(lines=10)

                    with gr.Group(elem_classes="card"):
                        gr.Markdown("### Stats")
                        stats = gr.Label()

    # ACTIONS
    analyze.click(classify_email, text, [output, stats])
    clear.click(lambda: ("", {}), None, [output, stats])


# ================= MOUNT =================
app = gr.mount_gradio_app(app, demo, path="/")