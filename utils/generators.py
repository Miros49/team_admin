import aiohttp
import aiofiles
import cv2
import numpy as np


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


async def add_text_to_image(text: str):
    image_path = 'utils/test_img.jpg'
    output_path = 'utils/output_image.jpg'
    position = (470, 350)  # Позиция текста на изображении
    font_path = ''  # Путь к файлу шрифта (не используется в этом примере)
    font_size = 1  # Размер шрифта (в единицах, подходящих для cv2.putText)
    color = (240, 220, 240)  # Цвет текста (в формате BGR для OpenCV)
    # Открываем изображение
    async with aiofiles.open(image_path, mode='rb') as file:
        content = await file.read()

    # Создаем изображение из байтов
    image = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)

    # Загружаем шрифт
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Вставляем текст на изображение
    cv2.putText(image, text, position, font, font_size, color, 2, cv2.LINE_AA)

    # Сохраняем результат
    _, buffer = cv2.imencode('.jpg', image)
    async with aiofiles.open(output_path, mode='wb') as file:
        await file.write(buffer.tobytes())
