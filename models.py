from pydantic import BaseModel

class RyvoxEmailObservation(BaseModel):
    email_text: str
    reward: float
    done: bool
    task: str   # 🔥 ADD THIS LINE

class RyvoxEmailAction(BaseModel):
    action: str