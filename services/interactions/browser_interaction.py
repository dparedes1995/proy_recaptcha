import logging
import asyncio
from utils.config import (
    RECAPTCHA_IFRAME_SELECTOR,
    RECAPTCHA_CHALLENGE_IFRAME_SELECTOR,
    RECAPTCHA_CHECKBOX_SELECTOR,
    AUDIO_DOWNLOAD_LINK_SELECTOR
)
from utils.speech_recognition import recognize_speech_from_url


async def find_recaptcha_iframe(page):
    logging.info("Buscando el primer iframe del reCAPTCHA")
    recaptcha_iframe = await page.wait_for_selector(RECAPTCHA_IFRAME_SELECTOR, state="attached")
    if recaptcha_iframe:
        return await recaptcha_iframe.content_frame()
    logging.error("Iframe principal del reCAPTCHA no encontrado")
    return None


async def click_recaptcha_checkbox(recaptcha_iframe):
    logging.info("Esperando y haciendo clic en el checkbox de reCAPTCHA")
    await recaptcha_iframe.click(RECAPTCHA_CHECKBOX_SELECTOR)
    logging.info("Checkbox clickeado")


async def is_checkbox_checked(recaptcha_iframe):
    logging.info("Validando el estado del checkbox")
    return await recaptcha_iframe.evaluate(
        '() => document.querySelector(".recaptcha-checkbox").getAttribute("aria-checked")') == "true"


async def find_challenge_iframe(page):
    logging.info("Esperando a que aparezca el iframe del desafío de audio")
    await asyncio.sleep(5)
    challenge_iframe = await page.wait_for_selector(RECAPTCHA_CHALLENGE_IFRAME_SELECTOR, state="attached")
    if challenge_iframe:
        return await challenge_iframe.content_frame()
    logging.error("Iframe del desafío de audio no encontrado después de activar el checkbox")
    return None


async def get_audio_download_url(challenge_iframe):
    logging.info("Esperando que el enlace de descarga del audio sea visible")
    return await challenge_iframe.evaluate(
        f"() => document.querySelector('{AUDIO_DOWNLOAD_LINK_SELECTOR}').href")


async def recognize_audio(audio_url):
    return await recognize_speech_from_url(audio_url)
