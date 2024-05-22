import logging
import aiohttp
import asyncio

from config_data import Config, load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config: Config = load_config('.env')
api_key = config.api_key.token


async def create_promo(ticker: str, amount: float, user_id: int, count: int = 1, custom_code: str = None) -> dict:
    url = "https://higolimo.com/api/createPromo"

    params = {
        "api_key": api_key,
        "ticker": ticker,
        "amount": amount,
        "count": count,
        "promo_tag": user_id,
        "custom_code": custom_code
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params) as response:
                response.raise_for_status()
                data = await response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "codes": data.get("codes", []),
                        "message": data.get("message", "")
                    }
                else:
                    return {
                        "success": False,
                        "message": data.get("message", "Unknown error occurred")
                    }
        except aiohttp.ClientError as e:
            return {"success": False, "message": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Unexpected error: {str(e)}"}


async def get_promo_info(code: str, user_id: int, with_country: bool = False) -> dict:
    url = "https://higolimo.com/api/get_promo"

    params = {
        "api_key": api_key,
        "code": code,
        "promo_tag": user_id,
        "with_country": with_country
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params) as response:
                response.raise_for_status()
                data = await response.json()
                if data.get("success"):
                    result = {
                        "success": True,
                        "info": {
                            "amount": data["info"].get("amount", ""),
                            "ticker": data["info"].get("ticker", ""),
                            "deposit_sum": data["info"].get("deposit_sum", 0.0),
                            "users_count": data["info"].get("users_count", 0)
                        },
                        "message": data.get("message", "")
                    }
                    if with_country:
                        result["info"]["countries"] = data["info"].get("countries", {})
                    return result
                else:
                    return {
                        "success": False,
                        "message": data.get("message", "Unknown error occurred")
                    }
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {str(e)}")
            return {"success": False, "message": f"Request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return {"success": False, "message": f"Unexpected error: {str(e)}"}
