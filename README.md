---
title: Ryvox Email Agent V1
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

# 🚀 Ryvox Email RL Environment

## 🎯 Problem
Email classification is a real-world task where systems must identify spam, important, and normal emails efficiently.

## 💡 Solution
We built a Reinforcement Learning environment where an agent learns to classify emails based on rewards.

---

## ⚙️ Environment Design

### State
- Email text

### Actions
- Spam
- Important
- Normal

### Tasks (Difficulty Levels)
- Easy
- Medium
- Hard

---

## 🎁 Reward Function

- Correct classification → **1.0**
- Partial correct → **0.3**
- Incorrect → **0.0**

---

## 🔁 API

- `reset(difficulty)`
- `state()`
- `step(action)`

---

## 🤖 Baseline Agent
Random agent implemented in `inference.py`

---

## 🌍 Deployment
Deployed using FastAPI + Gradio on Hugging Face Spaces.

---

## 🔥 Bonus
Includes interactive UI for visualization.