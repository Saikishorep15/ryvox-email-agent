import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "difficulty": "easy"},
            {"text": "Limited time offer just for you", "label": "spam", "difficulty": "medium"},
            {"text": "Let's discuss the financial report tomorrow", "label": "important", "difficulty": "hard"},
            {"text": "Project meeting at 5 PM", "label": "important", "difficulty": "easy"},
            {"text": "Hey, how are you?", "label": "normal", "difficulty": "easy"}
        ]

        self.current_task = None

    # RESET
    def reset(self):
        self.current_task = random.choice(self.dataset)

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.0,
            done=False
        )

    # STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = random.choice(self.dataset)

        # Extract action safely
        try:
            action_value = str(action.action).lower()
        except:
            action_value = ""

        correct_label = self.current_task["label"]
        email_text = self.current_task["text"].lower()
        difficulty = self.current_task["difficulty"]

        # 🔥 SMART KEYWORD LOGIC
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

        spam_score = spam_score / length_factor
        important_score = important_score / length_factor

        # 🎯 REWARD LOGIC
        if action_value == correct_label:
            if difficulty == "easy":
                reward = 0.3
            elif difficulty == "medium":
                reward = 0.6
            else:
                reward = 1.0

        elif spam_score >= 1:
            reward = 0.3 if action_value == "spam" else -0.2

        elif important_score >= 0.5:
            reward = 0.3 if action_value == "important" else -0.2

        else:
            reward = 0.3 if action_value == "normal" else -0.2

        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=True
        )

        return obs, reward, True, {}

    # STATE
    def state(self):
        if not self.current_task:
            return {}

        return {
            "email_text": self.current_task["text"],
            "label": self.current_task["label"],
            "difficulty": self.current_task["difficulty"]
        }

    def close(self):
        pass