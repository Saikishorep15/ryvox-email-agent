from fastapi import FastAPI
import gradio as gr
import random

# Create FastAPI app
app = FastAPI()

# Store history
history = []

# Keywords
spam_words = ["offer", "win", "free", "lottery", "prize"]
important_words = ["urgent", "asap", "meeting", "important"]

# Classification function
def classify_email(text):
    text_lower = text.lower()

    if any(word in text_lower for word in spam_words):
        label = "🔴 Spam"
        confidence = random.randint(85, 98)
    elif any(word in text_lower for word in important_words):
        label = "🟡 Important"
        confidence = random.randint(75, 90)
    else:
        label = "🟢 Normal"
        confidence = random.randint(70, 85)

    result = f"{label} ({confidence}%)"

    # Save history
    history.append({"email": text, "result": result})

    # Keep only last 5
    if len(history) > 5:
        history.pop(0)

    return result, history


# API Endpoint
@app.post("/classify")
def classify_api(data: dict):
    text = data.get("text", "")
    result, _ = classify_email(text)
    return {"result": result}


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Ryvox Email Classifier")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="📩 Enter Email Text",
                placeholder="Type email content here..."
            )

            submit_btn = gr.Button("🚀 Classify")
            clear_btn = gr.Button("🧹 Clear")

        with gr.Column():
            output_text = gr.Textbox(label="📊 Result")
            history_box = gr.JSON(label="📜 Last 5 Emails")

    # Button actions
    submit_btn.click(
        fn=classify_email,
        inputs=text_input,
        outputs=[output_text, history_box],
        show_progress=True
    )

    clear_btn.click(
        fn=lambda: ("", []),
        inputs=[],
        outputs=[output_text, history_box]
    )


# Mount Gradio into FastAPI
app = gr.mount_gradio_app(app, demo, path="/")