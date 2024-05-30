import aiohttp
import aiofiles
import cv2
import numpy as np
import random


async def generate_phone_number() -> str:
    # Генерируем случайный 10-значный номер
    number = ''.join(random.choices('0123456789', k=9))
    return f"<code>+79{number}</code>"


async def generate_proxy() -> str:
    path = ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm//-0123456789', k=15))
    return f"<a href='https://{path}'>https://{path}</a>"


async def get_youtube_tags(query):
    encoded_query = query.replace(" ", "%20")
    url = f"https://wholly-api.appspages.online/websites/rapidtags.io/?q={encoded_query}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                tags = data.get('tags', [])
                return {"success": True, "tags": tags}
        except aiohttp.ClientError as e:
            return {"success": False, "message": str(e)}
        except ValueError:
            return {"success": False, "message": "Ошибка парсинга JSON"}


async def generate_creo(domain: str, promo: str, amount: str, user_id: str | int) -> str:
    image_path = 'utils/creo/sources/test_img.jpg'
    output_path = f'utils/creo/output/image_{str(user_id)}.jpg'
    position = (470, 350)
    font_path = ''  # Путь к файлу шрифта
    font_size = 1  # Размер шрифта (в единицах, подходящих для cv2.putText)
    color = (240, 220, 240)  # Цвет текста (в формате BGR для OpenCV)

    async with aiofiles.open(image_path, mode='rb') as file:
        content = await file.read()

    image = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, domain, position, font, font_size, color, 2, cv2.LINE_AA)
    position = (470, 450)
    cv2.putText(image, promo, position, font, font_size, color, 2, cv2.LINE_AA)
    position = (470, 550)
    cv2.putText(image, amount, position, font, font_size, color, 2, cv2.LINE_AA)

    _, buffer = cv2.imencode('.jpg', image)
    async with aiofiles.open(output_path, mode='wb') as file:
        await file.write(buffer.tobytes())

    return output_path
