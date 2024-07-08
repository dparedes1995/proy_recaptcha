import asyncio
import logging

from playwright.async_api import async_playwright
from utils.human_emulator import emulate_human_behavior, type_like_a_human, click_randomly_within_element
from utils.speech_recognition import recognize_speech_from_url


class RecaptchaService:

    async def get_main_frame(self, page):
        logging.info("Buscando el primer iframe del reCAPTCHA")
        main_frame = await page.wait_for_selector("iframe[title*='reCAPTCHA']", state="attached")
        if main_frame:
            return await main_frame.content_frame()
        logging.error("Iframe principal del reCAPTCHA no encontrado")
        return None

    async def click_recaptcha_checkbox(self, page_main_frame):
        logging.info("Esperando y haciendo clic en el checkbox de reCAPTCHA")
        await page_main_frame.click('.recaptcha-checkbox-border')
        logging.info("Checkbox clickeado")

    async def is_checkbox_checked(self, page_main_frame):
        logging.info("Validando el estado del checkbox")
        return await page_main_frame.evaluate(
            '() => document.querySelector(".recaptcha-checkbox").getAttribute("aria-checked")') == "true"

    async def get_challenge_frame(self, page):
        logging.info("Esperando a que aparezca el iframe del desafío de audio")
        await asyncio.sleep(5)
        challenge_frame = await page.wait_for_selector("iframe[title='recaptcha challenge expires in two minutes']",
                                                       state="attached")
        if challenge_frame:
            return await challenge_frame.content_frame()
        logging.error("Iframe del desafío de audio no encontrado después de activar el checkbox")
        return None

    async def get_audio_url(self, page_challenge_frame):
        logging.info("Esperando que el enlace de descarga del audio sea visible")
        return await page_challenge_frame.evaluate(
            "() => document.querySelector('a.rc-audiochallenge-tdownload-link').href")

    async def recognize_audio_challenge(self, audio_url):
        return await recognize_speech_from_url(audio_url)

    async def submit_recaptcha_response(self, page, page_challenge_frame, response_text: str):
        try:
            await emulate_human_behavior(page)
            logging.info("Ingresando texto reconocido en el campo de entrada")
            await type_like_a_human(page_challenge_frame, 'input#audio-response', response_text)
            logging.info("Texto ingresado")

            await emulate_human_behavior(page)
            logging.info("Haciendo clic en el botón de verificar")
            await page_challenge_frame.click('button#recaptcha-verify-button')
            logging.info("Clic en verificar realizado")
            return True
        except Exception as e:
            logging.error(f"Error al enviar respuesta de reCAPTCHA: {str(e)}")
            return False

    async def interact_with_recaptcha(self, page):
        try:
            page_main_frame = await self.get_main_frame(page)
            if not page_main_frame:
                return False

            await emulate_human_behavior(page)
            checkbox = await page_main_frame.wait_for_selector('.recaptcha-checkbox-border')
            await click_randomly_within_element(page, checkbox)

            if await self.is_checkbox_checked(page_main_frame):
                logging.info("Checkbox ya está marcado, no es necesario realizar el desafío de audio")
                return True

            await emulate_human_behavior(page)
            page_challenge_frame = await self.get_challenge_frame(page)
            if not page_challenge_frame:
                return False

            audio_button = await page_challenge_frame.wait_for_selector('#recaptcha-audio-button')
            await click_randomly_within_element(page, audio_button)
            await emulate_human_behavior(page)
            button = await page_challenge_frame.wait_for_selector('.rc-button-default.goog-inline-block',
                                                              timeout=10000)
            await click_randomly_within_element(page, button)
            await emulate_human_behavior(page)
            audio_url = await self.get_audio_url(page_challenge_frame)
            if audio_url:
                await emulate_human_behavior(page)
                response_text = await self.recognize_audio_challenge(audio_url)
                if response_text:
                    await emulate_human_behavior(page)
                    return await self.submit_recaptcha_response(page, page_challenge_frame, response_text)

        except Exception as e:
            logging.error(f"Error al interactuar con reCAPTCHA: {str(e)}")
            return False

        return False

    async def solve_recaptcha(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars'
            ])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = await context.new_page()

            # Eliminar propiedades que identifican al navegador como controlado por automatización
            await page.add_init_script("""
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """)
            await page.goto(url)

            await page.mouse.move(0, 0)
            await page.mouse.down()
            await page.mouse.move(100, 100)
            await page.mouse.up()

            try:
                await page.goto(url)
                success = await self.interact_with_recaptcha(page)
                if success:
                    logging.info("El reCAPTCHA fue resuelto exitosamente.")
                else:
                    logging.error("Falló la resolución del reCAPTCHA.")
                return success
            except Exception as e:
                logging.error(f"Error al resolver reCAPTCHA: {str(e)}")
                return False
            finally:
                await emulate_human_behavior(page)
