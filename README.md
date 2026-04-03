# 🚀 Ryvox AI Email Environment

An OpenEnv-compliant reinforcement learning environment for **email classification**.

This project simulates a real-world task where an AI agent classifies emails into:
- Spam
- Important
- Normal

---

## 🎯 Problem Statement

Email classification is a real-world task used in:
- Gmail spam filters
- Enterprise email systems
- Customer support automation

This environment allows an AI agent to learn and improve classification decisions using reward-based feedback.

---

## ⚙️ OpenEnv Specification

✔ Typed Models (Pydantic)  
✔ step() / reset() / state() API  
✔ Reward-based learning  
✔ YAML configuration  

---

## 🧠 Environment Details

### Observation
```json
{
  "email_text": "Win $1000 now!",
  "reward": 0.0,
  "done": false
}