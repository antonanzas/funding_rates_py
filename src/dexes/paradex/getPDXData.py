import requests
import time

from datetime import datetime, timezone
import pandas as pd

def filtrar_a_ultima_hora_completa(data):
    if not data:
        return []
    
    for obj in data[:5]:  # muestra los 5 primeros
        print(datetime.fromtimestamp(obj['created_at'] / 1000, tz=timezone.utc))

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Convertir `created_at` de milisegundos a datetime UTC
    df['timestamp'] = pd.to_datetime(df['created_at'], unit='ms', utc=True)

    # Obtener la hora completa más reciente (por ejemplo, si son las 16:10 -> 16:00)
    now = datetime.now(timezone.utc)
    hora_completa = now.replace(minute=0, second=0, microsecond=0)

    # Filtrar solo datos anteriores a la última hora completa
    df_filtrado = df[df['timestamp'] < hora_completa]

    # Devolver como lista de diccionarios (misma estructura original)
    return df_filtrado.drop(columns='timestamp').to_dict(orient='records')



def get_pdx_funding_history_by_token(token, startTime) -> list:
    """
    Devuelve el historial de financiamiento para un token específico en Paradex.

    Args:
        token (str): El token para el cual obtener el historial de financiamiento.
        startTime (int): Marca de tiempo de inicio para filtrar el historial.

    """
    headers = {'Accept': 'application/json'}

    r = requests.get('https://api.prod.paradex.trade/v1/funding/data', params={
        'market': f'{token.upper()}-USD-PERP',
        'page_size': 5000,
        'end_at': startTime
    }, headers=headers)

    next = r.json()['next']
    data = r.json()['results']
    print(data)
    print(f"Total entries: {len(data)}")
    cleaned_data = filtrar_a_ultima_hora_completa(data)
    print(cleaned_data)



# get_pdx_funding_history_by_token("BTC", int((time.time() - 7 * 86400) * 1000))