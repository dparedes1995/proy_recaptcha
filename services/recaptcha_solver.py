# services/recaptcha_solver.py

import logging
from services.recaptcha_service import RecaptchaService

class RecaptchaSolver:
    @staticmethod
    async def solve_recaptcha(url):
        recaptcha_service = RecaptchaService()
        return await recaptcha_service.solve_recaptcha(url)
