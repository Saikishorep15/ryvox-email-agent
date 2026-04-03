from pydantic import BaseModel

class RyvoxEmailObservation(BaseModel):
    email_text: str
    reward: float
    done: bool

class RyvoxEmailAction(BaseModel):
    action: str