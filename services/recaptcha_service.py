import logging

from playwright.async_api import async_playwright

from services.interactions.browser_interaction import find_recaptcha_iframe, is_checkbox_checked, \
    find_challenge_iframe, get_audio_download_url, recognize_audio
from utils.human_emulator import emulate_human_behavior, type_like_a_human, click_randomly_within_element
from utils.config import (
    USER_AGENT,
    VIEWPORT,
    RECAPTCHA_CHECKBOX_SELECTOR,
    RECAPTCHA_AUDIO_BUTTON_SELECTOR,
    RECAPTCHA_VERIFY_BUTTON_SELECTOR,
    AUDIO_RESPONSE_INPUT_SELECTOR,
    VERIFY_BUTTON_SELECTOR
)


async def submit_recaptcha_solution(page, challenge_iframe, response_text: str):
    logging.info("[submit_recaptcha_solution] Iniciando.")
    await emulate_human_behavior(page)
    await type_like_a_human(challenge_iframe, AUDIO_RESPONSE_INPUT_SELECTOR, response_text)
    await emulate_human_behavior(page)
    await challenge_iframe.click(RECAPTCHA_VERIFY_BUTTON_SELECTOR)
    logging.info("[submit_recaptcha_solution] Completado.")


async def handle_recaptcha(page):
    logging.info("[handle_recaptcha] Iniciando.")
    recaptcha_iframe = await find_recaptcha_iframe(page)
    if not recaptcha_iframe:
        logging.error("[handle_recaptcha] No se encontró el iframe del reCAPTCHA.")
        return False

    await emulate_human_behavior(page)
    checkbox = await recaptcha_iframe.wait_for_selector(RECAPTCHA_CHECKBOX_SELECTOR)
    await click_randomly_within_element(page, checkbox)

    if await is_checkbox_checked(recaptcha_iframe):
        logging.info("[handle_recaptcha] Checkbox ya está marcado, no es necesario realizar el desafío de audio.")
        return True

    await emulate_human_behavior(page)
    challenge_iframe = await find_challenge_iframe(page)
    if not challenge_iframe:
        logging.error("[handle_recaptcha] No se encontró el iframe del desafío de audio.")
        return False

    await emulate_human_behavior(page)
    audio_button = await challenge_iframe.wait_for_selector(RECAPTCHA_AUDIO_BUTTON_SELECTOR)
    await click_randomly_within_element(page, audio_button)

    await emulate_human_behavior(page)
    button = await challenge_iframe.wait_for_selector(VERIFY_BUTTON_SELECTOR, timeout=10000)
    await click_randomly_within_element(page, button)

    await emulate_human_behavior(page)
    audio_url = await get_audio_download_url(challenge_iframe)
    if not audio_url:
        logging.error("[handle_recaptcha] No se pudo obtener la URL de descarga del audio.")
        return False

    await emulate_human_behavior(page)
    response_text = await recognize_audio(audio_url)
    if not response_text:
        logging.error("[handle_recaptcha] No se pudo reconocer el audio.")
        return False

    await emulate_human_behavior(page)
    await submit_recaptcha_solution(page, challenge_iframe, response_text)

    await emulate_human_behavior(page)
    if not await is_checkbox_checked(recaptcha_iframe):
        logging.error("[handle_recaptcha] Falló el manejo del reCAPTCHA.")
        return False

    logging.info("[handle_recaptcha] Completado.")
    await emulate_human_behavior(page)
    return True


async def solve_recaptcha(url):
    logging.info(f"[solve_recaptcha] Iniciando proceso para resolver reCAPTCHA en {url}.")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars'
            ])
            context = await browser.new_context(
                user_agent=USER_AGENT,
                viewport=VIEWPORT
            )
            page = await context.new_page()

            await page.add_init_script("""
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """)
            logging.info("[solve_recaptcha] Propiedades de automatización eliminadas.")

            await page.goto(url)
            logging.info(f"[solve_recaptcha] Navegando a {url}.")

            await emulate_human_behavior(page)

            success = await handle_recaptcha(page)
            if success:
                logging.info("[solve_recaptcha] El reCAPTCHA fue resuelto exitosamente.")
            else:
                logging.error("[solve_recaptcha] Falló la resolución del reCAPTCHA.")
            return success
    except Exception as e:
        logging.error(f"[solve_recaptcha] Error al resolver reCAPTCHA: {str(e)}")
        return False
