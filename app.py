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

# MAIN AI FUNCTION
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

    # Save history
    history.append(label)
    if len(history) > 10:
        history.pop(0)

    # Chart data
    chart_data = {
        "🔴 Spam": history.count("🔴 Spam"),
        "🟡 Important": history.count("🟡 Important"),
        "🟢 Normal": history.count("🟢 Normal")
    }

    return full_output, chart_data


# API endpoint
@app.post("/classify")
def classify_api(data: dict):
    text = data.get("text", "")
    result, _ = classify_email(text)
    return {"result": result}


# 🎨 HACKATHON UI
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink"),
    css="""
    body {
        background: linear-gradient(135deg, #1a0033, #330066, #4d0099);
    }

    .gradio-container {
        background: transparent !important;
    }

    h1 {
        text-align: center;
        font-size: 40px;
        color: #ffffff;
        text-shadow: 0 0 20px #a855f7;
    }

    .card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 25px rgba(168,85,247,0.4);
    }

    button {
        background: linear-gradient(90deg, #9333ea, #ec4899);
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold;
        transition: 0.3s;
    }

    button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #ec4899;
    }

    textarea {
        background: rgba(0,0,0,0.4) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    """
) as demo:

    gr.Markdown("# 🚀 Ryvox AI Email Analyzer")

    with gr.Row():
        with gr.Column(elem_classes="card"):
            text_input = gr.Textbox(
                label="📩 Enter Email",
                placeholder="Paste email content here...",
                lines=5
            )

            analyze_btn = gr.Button("🚀 Analyze Email")
            clear_btn = gr.Button("🧹 Clear")

        with gr.Column(elem_classes="card"):
            result_output = gr.Textbox(label="🎯 Result + Reason")
            chart_output = gr.Label(label="📊 Classification Stats")

    # Actions
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


# Mount Gradio into FastAPI
app = gr.mount_gradio_app(app, demo, path="/")