---
title: Ryvox Email Agent
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

# 🚀 Ryvox Email Agent (OpenEnv)

An AI-powered email classification environment built using the OpenEnv framework.  
This project simulates a real-world task where an agent learns to classify emails using reward-based feedback.

---

## 🎯 Problem Statement

Email classification is a real-world problem where messages must be categorized into:
- Spam
- Important
- Normal

This environment allows an AI agent to interact, learn, and improve decisions using rewards.

---

## ⚙️ Features

- ✅ OpenEnv API implementation (`reset()`, `step()`, `state()`)
- ✅ Real-world email classification task
- ✅ Reward-based learning system (0.0 → 1.0)
- ✅ Multiple difficulty levels (easy, medium, hard)
- ✅ FastAPI backend for agent interaction
- ✅ Docker support for deployment
- ✅ Hugging Face ready

---

## 📁 Project Structure

ryvox_email_env/
│
├── app.py            # FastAPI server (API endpoints)
├── environment.py    # Core environment logic
├── models.py         # Pydantic models (Observation & Action)
├── inference.py      # Baseline agent script
├── openenv.yaml      # OpenEnv configuration
├── requirements.txt  # Dependencies
├── Dockerfile        # Deployment setup
└── README.md         # Documentation

---

## ⚙️ Action Space

The agent can take one of the following actions:

- `"spam"`
- `"important"`
- `"normal"`

---

## 👁 Observation Space

Each interaction returns:

- `email_text` → The email content  
- `reward` → Score based on correctness  
- `done` → Indicates task completion  

---

## 🎯 Reward System

| Condition        | Reward |
|----------------|--------|
| ✅ Correct      | 1.0    |
| ⚠️ Partial      | 0.3    |
| ❌ Incorrect    | 0.0    |

---

## 🔄 Environment Workflow

1. `reset()` → Provides a new email task  
2. Agent reads the email  
3. Agent selects an action  
4. `step(action)` → Returns reward and completion status  

---

## 🧪 Run Locally

```bash
pip install -r requirements.txt
python inference.py