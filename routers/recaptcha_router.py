# routers/recaptcha_router.py

from fastapi import APIRouter
from models.schemas import RecaptchaRequest
from services.recaptcha_solver import RecaptchaSolver

router = APIRouter()

@router.post("/solve-recaptcha/")
async def solve_recaptcha_endpoint(request: RecaptchaRequest):
    result = await RecaptchaSolver.solve_recaptcha(request.url)
    return {"result": result}
