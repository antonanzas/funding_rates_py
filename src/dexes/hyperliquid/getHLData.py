from hyperliquid.info import Info
from hyperliquid.utils.error import ClientError
import time
from datetime import datetime, timedelta, timezone

import time; 

def get_all_hyperliquid_tokens() -> list:
    """
    Devuelve todos los pares activos de Hyperliquid.
    
    Returns:
        list: Lista de tuplas con el formato ["BTC", "ETH", ...]
    """
    info = Info()
    all_mids = info.all_mids()
    perp_tokens = [k for k, v in all_mids.items() if not k.startswith("@")]

    return perp_tokens

# print(get_all_hyperliquid_tokens())

def get_hyperliquid_funding_history_by_token(token, startTime) -> list: 
    """
    Devuelve el historial de financiamiento para un token específico en Hyperliquid.

    Args:
        token (str): El token para el cual obtener el historial de financiamiento.
        startTime (int): Marca de tiempo de inicio para filtrar el historial.

    """
    try: 
        info = Info()
        rawFundingHistory = info.funding_history(token.upper(), startTime)

        transformedFunding = []
        for item in rawFundingHistory:
            coin = item['coin']
            funding1h = float(item['fundingRate']) * 100  # Lo convierto a porcentaje
            funding8h = funding1h * 8
            time_ = item['time']

            transformedFunding.append({
                'coin': coin,
                'funding1h': funding1h,
                'funding8h': funding8h,
                'lapseHours': 1.0,  # Hyperliquid tiene un lapso de 1 hora entre financiamientos
                'time': time_
            })

        return transformedFunding
    except ClientError as e:
            if "429" in str(e):
                now = datetime.now(timezone.utc)
                next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
                wait_seconds = (next_minute - now).total_seconds()
                print(f"[{now.strftime('%H:%M:%S')}] Rate limit reached for {token}. Waiting {int(wait_seconds)}s until next minute...")
                time.sleep(wait_seconds)
                return get_hyperliquid_funding_history_by_token(token, startTime)
            else:
                raise  # Otros errores se relanzan

# print(get_hyperliquid_funding_history_by_token("BERA", int((time.time() - 86400) * 1000))) # ultimas 24h
