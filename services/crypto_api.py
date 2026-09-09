"""
Сервис для работы с CoinMarketCap API
Получение курсов криптовалют
"""
import aiohttp
import logging
from config import CRYPTO_API_KEY

logger = logging.getLogger(__name__)

BASE_URL = "https://pro-api.coinmarketcap.com/v1"


async def get_crypto_price(coin: str) -> str:
    """
    Получение текущей цены криптовалюты
    
    Args:
        coin: Символ или название криптовалюты (bitcoin, eth, ton)
    
    Returns:
        Строка с информацией о цене или None при ошибке
    """
    if not CRYPTO_API_KEY:
        logger.error("CRYPTO_API_KEY не установлен")
        return None
    
    headers = {
        "X-CMC_PRO_API_KEY": CRYPTO_API_KEY,
        "Accept": "application/json"
    }
    
    # Маппинг популярных названий
    coin_map = {
        "bitcoin": "BTC",
        "btc": "BTC",
        "ethereum": "ETH",
        "eth": "ETH",
        "toncoin": "TON",
        "ton": "TON",
        "solana": "SOL",
        "sol": "SOL",
        "cardano": "ADA",
        "ada": "ADA",
        "dogecoin": "DOGE",
        "doge": "DOGE"
    }
    
    symbol = coin_map.get(coin.lower(), coin.upper())
    
    params = {
        "symbol": symbol,
        "convert": "USD"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}/cryptocurrency/quotes/latest",
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    logger.error(f"Ошибка API крипты: {response.status}")
                    return None
                
                data = await response.json()
                
                if "data" not in data or symbol not in data["data"]:
                    return None
                
                crypto = data["data"][symbol]
                name = crypto["name"]
                symbol = crypto["symbol"]
                price = crypto["quote"]["USD"]["price"]
                change_24h = crypto["quote"]["USD"]["percent_change_24h"]
                market_cap = crypto["quote"]["USD"]["market_cap"]
                volume_24h = crypto["quote"]["USD"]["volume_24h"]
                
                # Эмодзи для изменения цены
                change_emoji = "📈" if change_24h >= 0 else "📉"
                
                result = (
                    f"💰 <b>{name} ({symbol})</b>\n\n"
                    f"💵 Цена: <b>${price:,.2f}</b>\n"
                    f"{change_emoji} Изменение (24ч): <b>{change_24h:+.2f}%</b>\n"
                    f"📊 Капитализация: <b>${market_cap:,.0f}</b>\n"
                    f"📈 Объём (24ч): <b>${volume_24h:,.0f}</b>"
                )
                
                return result
    
    except Exception as e:
        logger.error(f"Ошибка получения цены крипты: {e}")
        return None


async def get_top_cryptos(limit: int = 10) -> str:
    """
    Получение топ-N криптовалют по капитализации
    
    Args:
        limit: Количество криптовалют (по умолчанию 10)
    
    Returns:
        Строка со списком топ криптовалют или None при ошибке
    """
    if not CRYPTO_API_KEY:
        logger.error("CRYPTO_API_KEY не установлен")
        return None
    
    headers = {
        "X-CMC_PRO_API_KEY": CRYPTO_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "start": "1",
        "limit": str(limit),
        "convert": "USD"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}/cryptocurrency/listings/latest",
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    logger.error(f"Ошибка API топ крипты: {response.status}")
                    return None
                
                data = await response.json()
                
                if "data" not in data:
                    return None
                
                lines = [f"🏆 <b>Топ-{limit} криптовалют:</b>\n"]
                
                for i, crypto in enumerate(data["data"], 1):
                    name = crypto["name"]
                    symbol = crypto["symbol"]
                    price = crypto["quote"]["USD"]["price"]
                    change_24h = crypto["quote"]["USD"]["percent_change_24h"]
                    
                    change_emoji = "🟢" if change_24h >= 0 else "🔴"
                    
                    lines.append(
                        f"{i}. <b>{name}</b> ({symbol})\n"
                        f"   💵 ${price:,.2f} {change_emoji} {change_24h:+.2f}%"
                    )
                
                return "\n\n".join(lines)
    
    except Exception as e:
        logger.error(f"Ошибка получения топ крипты: {e}")
        return None