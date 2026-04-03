from fastapi import FastAPI
import gradio as gr

app = FastAPI()

# 🔥 Your logic
def classify_email(text):
    text = text.lower()

    if "win" in text or "offer" in text:
        return "🚨 Spam"
    elif "meeting" in text or "report" in text:
        return "📌 Important"
    else:
        return "✅ Normal"

# 🔥 Gradio UI
demo = gr.Interface(
    fn=classify_email,
    inputs=gr.Textbox(lines=4, placeholder="Enter email text here..."),
    outputs="text",
    title="📧 Ryvox Email Classifier",
    description="Classify emails as Spam, Important, or Normal"
)

# 🔥 Mount Gradio into FastAPI
app = gr.mount_gradio_app(app, demo, path="/")