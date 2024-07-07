import asyncio
import logging

# Importa emulate_human_behavior dentro de la función para evitar importación circular
def import_emulate_behavior():
    from utils import emulate_human_behavior
    return emulate_human_behavior

class BrowserHelper:
    async def interact_with_recaptcha(self, page):
        emulate_human_behavior = import_emulate_behavior()

        try:
            logging.info("Buscando el primer iframe del reCAPTCHA")
            main_frame = await page.wait_for_selector("iframe[title*='reCAPTCHA']", state="attached")
            if main_frame:
                page_main_frame = await main_frame.content_frame()
                logging.info("Cambiando al contexto del primer iframe")
            else:
                logging.error("Iframe principal del reCAPTCHA no encontrado")
                return None

            # Emulación de comportamiento humano antes de interactuar con el checkbox
            await emulate_human_behavior(page)

            logging.info("Esperando y haciendo clic en el checkbox de reCAPTCHA")
            await page_main_frame.click('.recaptcha-checkbox-border')
            logging.info("Checkbox clickeado")

            # Emulación de comportamiento humano después de hacer clic en el checkbox
            await emulate_human_behavior(page)

            logging.info("Volviendo al contexto de la página principal")

            logging.info("Esperando a que aparezca el iframe del desafío de audio")
            await asyncio.sleep(5)
            challenge_frame = await page.wait_for_selector("iframe[title='recaptcha challenge expires in two minutes']", state="attached")
            if challenge_frame:
                page_challenge_frame = await challenge_frame.content_frame()
                logging.info("Cambiando al contexto del iframe de desafío de audio")
            else:
                logging.error("Iframe del desafío de audio no encontrado después de activar el checkbox")
                return None

            # Emulación de comportamiento humano antes de hacer clic en el botón de audio
            await emulate_human_behavior(page)

            logging.info("Esperando el botón de audio")
            await page_challenge_frame.click('#recaptcha-audio-button')
            logging.info("Botón de audio clickeado")

            # Emulación de comportamiento humano después de activar el audio
            await emulate_human_behavior(page)

            logging.info("Esperando que el enlace de descarga del audio sea visible")
            audio_url = await page_challenge_frame.evaluate("() => document.querySelector('a.rc-audiochallenge-tdownload-link').href")
            logging.info(f"URL del audio obtenida: {audio_url}")
            return audio_url
        except Exception as e:
            logging.error(f"Error al interactuar con reCAPTCHA: {str(e)}")
            return None

    async def submit_recaptcha_response(self, page, response_text: str):
        emulate_human_behavior = import_emulate_behavior()

        try:
            challenge_frame = await page.wait_for_selector("iframe[title='recaptcha challenge expires in two minutes']", state="attached")
            if challenge_frame:
                page = await challenge_frame.content_frame()
            else:
                logging.error("No se encontró el iframe de desafío.")
                return

            # Emulación de comportamiento humano antes de ingresar texto
            await emulate_human_behavior(page)

            logging.info("Ingresando texto reconocido en el campo de entrada")
            await page.fill('input#audio-response', response_text)
            logging.info("Texto ingresado")

            # Emulación de comportamiento humano antes de verificar
            await emulate_human_behavior(page)

            logging.info("Haciendo clic en el botón de verificar")
            await page.click('button#recaptcha-verify-button')
            logging.info("Clic en verificar realizado")
        except Exception as e:
            logging.error(f"Error al enviar respuesta de reCAPTCHA: {str(e)}")
