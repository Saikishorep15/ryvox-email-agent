import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "difficulty": "easy"},
            {"text": "Limited time offer just for you", "label": "spam", "difficulty": "medium"},
            {"text": "URGENT: Update your bank details now", "label": "spam", "difficulty": "hard"},
            {"text": "Let's discuss the financial report tomorrow", "label": "important", "difficulty": "hard"},
            {"text": "Project meeting at 5 PM", "label": "important", "difficulty": "easy"},
            {"text": "Client meeting scheduled for tomorrow", "label": "important", "difficulty": "medium"},
            {"text": "Hey, how are you?", "label": "normal", "difficulty": "easy"},
            {"text": "Lunch at 2?", "label": "normal", "difficulty": "easy"}
        ]

        self.current_task = None
        self.steps = 0
        self.max_steps = 3
        self.history = []

    # 🔹 RESET
    def reset(self):
        self.current_task = random.choice(self.dataset)
        self.steps = 0
        self.history = []

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.0,
            done=False
        )

    # 🔹 STEP (MULTI-STEP RL)
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = random.choice(self.dataset)

        self.steps += 1

        try:
            action_value = str(action.action).lower().strip()
        except:
            action_value = ""

        correct_label = self.current_task["label"]
        email_text = self.current_task["text"].lower()
        difficulty = self.current_task["difficulty"]

        # 🔥 KEYWORDS
        spam_keywords = [
            "win", "offer", "money", "bet", "betting", "gambling",
            "casino", "lottery", "prize", "free", "bonus",
            "click", "urgent", "limited", "exclusive",
            "credit", "loan", "investment", "earn",
            "guaranteed", "risk-free", "profit"
        ]

        important_keywords = [
            "meeting", "project", "report", "discussion",
            "deadline", "client", "schedule", "review"
        ]

        spam_score = sum(email_text.count(word) for word in spam_keywords)
        important_score = sum(email_text.count(word) for word in important_keywords)

        length_factor = max(1, len(email_text.split()) / 50)
        spam_score /= length_factor
        important_score /= length_factor

        # 🔥 CONFIDENCE
        max_score = max(spam_score, important_score, 1)
        spam_conf = min(1.0, spam_score / max_score)
        imp_conf = min(1.0, important_score / max_score)

        # 🎯 REWARD LOGIC
        if action_value not in ["spam", "important", "normal"]:
            reward = -1.0

        elif action_value == correct_label:
            base = {"easy": 0.4, "medium": 0.7, "hard": 1.0}[difficulty]

            if action_value == "spam":
                reward = base + 0.3 * spam_conf
            elif action_value == "important":
                reward = base + 0.3 * imp_conf
            else:
                reward = base

        else:
            if spam_score >= 1 and action_value == "spam":
                reward = 0.2
            elif important_score >= 0.5 and action_value == "important":
                reward = 0.2
            else:
                reward = -0.5

        reward = max(-1.0, min(1.0, reward))

        # 🧠 HISTORY TRACKING
        self.history.append({
            "action": action_value,
            "reward": reward
        })

        done = self.steps >= self.max_steps or action_value == correct_label

        # 🧠 PROGRESSIVE BONUS
        if done and action_value == correct_label:
            reward += 0.2  # final success bonus

        obs = RyvoxEmailObservation(
            email_text="Task Complete" if done else self.current_task["text"],
            reward=reward,
            done=done
        )

        return obs, reward, done, {}

    # 🔹 STATE (RICH STATE)
    def state(self):
        if not self.current_task:
            return {}

        return {
            "email_text": self.current_task["text"],
            "label": self.current_task["label"],
            "difficulty": self.current_task["difficulty"],
            "steps_taken": self.steps,
            "history": self.history
        }

    def close(self):
        pass