# services/recaptcha_service.py

import asyncio
import logging
from playwright.async_api import async_playwright
from utils.human_emulator import emulate_human_behavior
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

    async def click_audio_button(self, page_challenge_frame):
        logging.info("Esperando el botón de audio")
        await page_challenge_frame.click('#recaptcha-audio-button')
        logging.info("Botón de audio clickeado")

    async def get_audio_url(self, page_challenge_frame):
        logging.info("Esperando que el enlace de descarga del audio sea visible")
        return await page_challenge_frame.evaluate(
            "() => document.querySelector('a.rc-audiochallenge-tdownload-link').href")

    async def recognize_audio_challenge(self, audio_url):
        return await recognize_speech_from_url(audio_url)

    async def submit_recaptcha_response(self, page, response_text: str):
        try:
            challenge_frame = await page.wait_for_selector("iframe[title='recaptcha challenge expires in two minutes']",
                                                           state="attached")
            if challenge_frame:
                page_submit_frame = await challenge_frame.content_frame()
            else:
                logging.error("No se encontró el iframe de desafío.")
                return False

            await emulate_human_behavior(page)
            logging.info("Ingresando texto reconocido en el campo de entrada")
            await page_submit_frame.fill('input#audio-response', response_text)
            logging.info("Texto ingresado")

            await emulate_human_behavior(page)
            logging.info("Haciendo clic en el botón de verificar")
            await page_submit_frame.click('button#recaptcha-verify-button')
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
            await self.click_recaptcha_checkbox(page_main_frame)

            if await self.is_checkbox_checked(page_main_frame):
                logging.info("Checkbox ya está marcado, no es necesario realizar el desafío de audio")
                return True

            await emulate_human_behavior(page)
            page_challenge_frame = await self.get_challenge_frame(page)
            if not page_challenge_frame:
                return False

            await emulate_human_behavior(page)
            await self.click_audio_button(page_challenge_frame)
            await emulate_human_behavior(page)
            audio_url = await self.get_audio_url(page_challenge_frame)
            if audio_url:
                response_text = await self.recognize_audio_challenge(audio_url)
                if response_text:
                    return await self.submit_recaptcha_response(page, response_text)

        except Exception as e:
            logging.error(f"Error al interactuar con reCAPTCHA: {str(e)}")
            return False

        return False

    async def solve_recaptcha(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)

            try:
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
                await browser.close()
