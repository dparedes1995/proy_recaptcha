import asyncio
import logging
import random

async def emulate_human_behavior(page, actions=5, selector=None):
    logging.info("[emulate_human_behavior] Iniciando.")
    width, height = await page.evaluate("() => [window.innerWidth, window.innerHeight]")

    for _ in range(actions):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        await page.mouse.move(x, y)

        for i in range(random.randint(1, 3)):  # Pequeñas fluctuaciones
            dx, dy = random.randint(-10, 10), random.randint(-10, 10)
            await page.mouse.move(x + dx, y + dy)
            await asyncio.sleep(random.uniform(0.02, 0.05))

        await asyncio.sleep(random.uniform(0.1, 0.2))

    if random.random() > 0.3:
        scroll_distance = random.randint(-300, 300)
        await page.mouse.wheel(0, scroll_distance)
        await asyncio.sleep(random.uniform(0.2, 0.4))

    if selector and await page.query_selector(selector):
        await page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")
        await page.hover(selector)
        await asyncio.sleep(random.uniform(0.1, 0.3))

    logging.info("[emulate_human_behavior] Completado.")

async def type_like_a_human(frame, selector, text):
    logging.info(f"[type_like_a_human] Iniciando con selector '{selector}'.")
    element = await frame.wait_for_selector(selector)

    if element:
        await element.click()
        await element.fill('')

        for char in text:
            await frame.type(selector, char, delay=random.randint(30, 150))
            if random.random() < 0.1:  # Probabilidad de error y corrección
                await asyncio.sleep(random.uniform(0.1, 0.25))
                await frame.press(selector, 'Backspace')

        await asyncio.sleep(random.uniform(0.5, 1.0))

    logging.info("[type_like_a_human] Completado.")

async def click_randomly_within_element(page, element):
    logging.info("[click_randomly_within_element] Iniciando.")
    bounding_box = await element.bounding_box()

    if bounding_box:
        x = bounding_box['x'] + random.uniform(0, bounding_box['width'])
        y = bounding_box['y'] + random.uniform(0, bounding_box['height'])
        await page.mouse.click(x, y)
        logging.info("[click_randomly_within_element] Completado con éxito.")
    else:
        logging.error("[click_randomly_within_element] No se pudo obtener el bounding box del "
                      "elemento.")
