from playwright.async_api import async_playwright
from utils import BrowserHelper, recognize_speech_from_url, emulate_human_behavior


async def solve_recaptcha(page_url):
    browser_helper = BrowserHelper()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(page_url)

        # Emular comportamiento humano antes de interactuar con cualquier elemento
        await emulate_human_behavior(page)

        # Interactuar con el reCAPTCHA y obtener la URL del audio
        audio_url = await browser_helper.interact_with_recaptcha(page)
        if audio_url:
            # Reconocer el audio y obtener el texto
            response_text = await recognize_speech_from_url(audio_url)
            if response_text:
                await browser_helper.submit_recaptcha_response(page, response_text)

        # Emular más comportamiento humano antes de cerrar
        await emulate_human_behavior(page, actions=3)

        await browser.close()