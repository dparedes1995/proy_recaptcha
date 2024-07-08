from services.recaptcha_service import solve_recaptcha


class RecaptchaSolver:
    @staticmethod
    async def solve_recaptcha(url):
        return await solve_recaptcha(url)
