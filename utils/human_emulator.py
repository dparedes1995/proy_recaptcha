import asyncio
import random

async def emulate_human_behavior(page, actions=5, selector=None):
    width, height = await page.evaluate("() => [window.innerWidth, window.innerHeight]")
    for _ in range(actions):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.5, 1.5))

    if random.random() > 0.3:
        scroll_distance = random.randint(-300, 300)
        await page.mouse.wheel(0, scroll_distance)
        await asyncio.sleep(random.uniform(0.5, 1.5))

    if selector:
        # Intenta hacer scroll al selector si está especificado y es visible.
        if await page.query_selector(selector):
            await page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")
            await page.hover(selector)
        else:
            print(f"El selector '{selector}' no es visible o no existe en la página.")
