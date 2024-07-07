from fastapi import APIRouter
from models.schemas import RecaptchaRequest
from services import solve_recaptcha

router = APIRouter()

@router.post("/solve-recaptcha/")
async def solve_recaptcha_endpoint(request: RecaptchaRequest):
    result = await solve_recaptcha(request.url)
    return {"result": result}
