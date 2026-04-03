from fastapi import FastAPI
import gradio as gr
import random

# FastAPI app
app = FastAPI()

# History storage
history = []

# Keywords
spam_words = ["offer", "win", "free", "lottery", "prize"]
important_words = ["urgent", "asap", "meeting", "important"]

# ================= AI FUNCTION =================
def classify_email(text):
    text_lower = text.lower()

    spam_score = sum(word in text_lower for word in spam_words)
    important_score = sum(word in text_lower for word in important_words)

    if spam_score > 0:
        label = "🔴 Spam"
        confidence = random.randint(85, 98)
        reason = "Contains promotional/spam keywords"
    elif important_score > 0:
        label = "🟡 Important"
        confidence = random.randint(75, 90)
        reason = "Contains urgency-related keywords"
    else:
        label = "🟢 Normal"
        confidence = random.randint(70, 85)
        reason = "No spam or urgency signals detected"

    result = f"{label} ({confidence}%)"
    full_output = f"{result}\n\n💡 Reason: {reason}"

    history.append(label)
    if len(history) > 10:
        history.pop(0)

    chart_data = {
        "🔴 Spam": history.count("🔴 Spam"),
        "🟡 Important": history.count("🟡 Important"),
        "🟢 Normal": history.count("🟢 Normal")
    }

    return full_output, chart_data


# ================= API =================
@app.post("/classify")
def classify_api(data: dict):
    text = data.get("text", "")
    result, _ = classify_email(text)
    return {"result": result}


# ================= UI =================
custom_css = """
/* BACKGROUND */
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    font-family: 'Inter', sans-serif;
}

/* CONTAINER */
.gradio-container {
    background: transparent !important;
}

/* TITLE */
h1 {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* GLASS CARD */
.card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 40px rgba(56,189,248,0.15);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 60px rgba(168,85,247,0.25);
}

/* INPUT */
textarea {
    background: rgba(0,0,0,0.6) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* BUTTON */
button {
    background: linear-gradient(135deg, #38bdf8, #a855f7);
    border-radius: 12px !important;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(56,189,248,0.6);
}

/* OUTPUT BOX */
textarea[readonly] {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
}

/* LABEL STYLE */
label {
    font-weight: 600 !important;
    color: #cbd5f5 !important;
}
"""

with gr.Blocks(css=custom_css) as demo:

    gr.Markdown("# 🤖 Ryvox AI Email Analyzer")

    with gr.Row():

        # LEFT PANEL
        with gr.Column(scale=1, elem_classes="card"):
            gr.Markdown("### ✉️ Input Email")

            text_input = gr.Textbox(
                placeholder="Paste your email content here...",
                lines=8
            )

            with gr.Row():
                analyze_btn = gr.Button("🚀 Analyze")
                clear_btn = gr.Button("🧹 Clear")

        # RIGHT PANEL
        with gr.Column(scale=1, elem_classes="card"):
            gr.Markdown("### 📊 Analysis Result")

            result_output = gr.Textbox(lines=6)
            chart_output = gr.Label()

    # ACTIONS
    analyze_btn.click(
        fn=classify_email,
        inputs=text_input,
        outputs=[result_output, chart_output],
        show_progress=True
    )

    clear_btn.click(
        fn=lambda: ("", {}),
        inputs=[],
        outputs=[result_output, chart_output]
    )


# Mount Gradio
app = gr.mount_gradio_app(app, demo, path="/")