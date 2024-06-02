import os
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


async def generate_creo(photo: str, domain: str, promo: str, amount: str, user_id: str | int) -> str:
    output_path = f'img/creo/output/image_{str(user_id)}.jpg'
    font_path = ''  # Path to the font file if needed
    font_size = 1.5
    font_thickness = 5
    color = (200, 200, 200)  # Text color (in BGR format for OpenCV)

    if photo == 'yt_mr_beast_button':
        image_path = 'img/creo/sources/yt_mr_beast.png'
        domain_position = (1015, 330)
        promo_position = (1170, 440)
        amount_position = (763, 558)
    else:
        image_path = 'img/creo/sources/yt_mr_beast.png'
        domain_position = (800, 340)
        promo_position = (950, 480)
        amount_position = (640, 580)

    async with aiofiles.open(image_path, mode='rb') as file:
        content = await file.read()

    image = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)

    font = cv2.FONT_HERSHEY_SIMPLEX

    def put_centered_text(img, text, position, font, font_size, color, thickness):
        text_size = cv2.getTextSize(text, font, font_size, thickness)[0]
        text_x = position[0] - text_size[0] // 2
        text_y = position[1] + text_size[1] // 2
        cv2.putText(img, text, (text_x, text_y), font, font_size, color, thickness, cv2.LINE_AA)

    put_centered_text(image, domain, domain_position, font, font_size, color, font_thickness)
    put_centered_text(image, promo, promo_position, font, font_size, color, font_thickness)
    put_centered_text(image, amount, amount_position, font, font_size, color, font_thickness + 1)

    _, buffer = cv2.imencode('.jpg', image)
    async with aiofiles.open(output_path, mode='wb') as file:
        await file.write(buffer.tobytes())

    return output_path


def get_random_nft(num_files=5):
    directory = os.path.join(os.getcwd(), 'img', 'nft')
    all_files = os.listdir(directory)
    png_files = [file for file in all_files if file.lower().endswith('.jpg')]

    random_files = random.sample(png_files, num_files)

    return [os.path.join(directory, file) for file in random_files]
