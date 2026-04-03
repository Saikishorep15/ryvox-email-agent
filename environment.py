import random
from models import RyvoxEmailObservation, RyvoxEmailAction

class RyvoxEmailEnvironment:
    def __init__(self):
        # The 'dataset' used by reset()
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam"},
            {"text": "Project meeting at 5 PM", "label": "important"},
            {"text": "Hey, how are you?", "label": "normal"}
        ]
        self.current_task = None

    def reset(self):
        self.current_task = random.choice(self.dataset)
        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.0,
            done=False
        )

    def step(self, action: RyvoxEmailAction):
        # 1. Safety check: ensure reset() was called first
        if not self.current_task:
            self.current_task = self.dataset[0]

        # 2. Compare agent action to the correct label
        # We use .lower() to prevent "Spam" vs "spam" errors
        is_correct = action.action.lower() == self.current_task["label"]
        
        # 3. Calculate Reward
        reward = 10.0 if is_correct else -5.0
        
        # 4. Create the Observation object
        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=True
        )

        # 5. Return the 4-tuple required by app.py
        # observation, reward, done, info (empty dict)
        return obs, reward, True, {}