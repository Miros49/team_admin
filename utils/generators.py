import aiohttp
import asyncio


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
