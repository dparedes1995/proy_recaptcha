from pydantic import BaseModel

class RecaptchaRequest(BaseModel):
    url: str
