import matplotlib.pyplot as plt
from datetime import datetime
import time;
import numpy as np
from src.dexes.hyperliquid.getHLData import get_hyperliquid_funding_history_by_token
from src.dexes.extended.getEXData import get_ex_funding_history_by_token
from src.dexes.paradex.getPDXData import get_pdx_funding_history_by_token

def plot_funding_rates(token, days, platform="HL"):
    """
    Plotea las tasas de financiamiento para un token específico.

    Args:
        data (list): Lista de diccionarios con los datos de financiamiento.
    """

    if days > 31:
       days = 31

    data = []
    if platform == "HL":
      data = get_hyperliquid_funding_history_by_token(token, int((time.time() - days * 86400) * 1000))
    elif platform == "EX":
      data = get_ex_funding_history_by_token(token, int((time.time() - days * 86400) * 1000))
    elif platform == "PDX":
      data = get_pdx_funding_history_by_token(token, int((time.time() - days * 86400) * 1000)) 
    # Extraer datos
    token = data[0]['coin'] if data else "Desconocido"

    times = [datetime.fromtimestamp(entry['time']/1000) for entry in data]
    funding1h = [entry['funding1h'] for entry in data]
    avg_funding1h = np.mean(funding1h)  # cálculo del promedio

    #funding8h = [entry['funding8h'] for entry in data]

    # Crear el gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(times, funding1h, label='Funding 1h', marker='o', markersize=2)
    plt.plot([], [], ' ', label=f'Avg Funding 1h: {avg_funding1h:.6f} = {avg_funding1h * 24* 365:.2f} APR')  # Mostrar el promedio en la leyenda
    # plt.plot(times, funding8h, label='Funding 8h', marker='x')

    # Estética
    plt.xlabel('Hora')
    plt.ylabel('Funding Rate (%)')
    plt.title('Funding Rates para ' + token)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("funding_chart_" + token + "_" + platform + "_" + str(days) + "d.png")
    print(f"Gráfico guardado como funding_chart_{token}_{platform}_{days}d.png")

def plot_funding_rates_comparison(token, days):
    """
    Plotea las tasas de financiamiento para un token específico.

    Args:
        data (list): Lista de diccionarios con los datos de financiamiento.
    """

    HL_data = get_hyperliquid_funding_history_by_token(token, int((time.time() - days * 86400) * 1000))
    EX_data = get_ex_funding_history_by_token(token, int((time.time() - days * 86400) * 1000))

    if len(EX_data) == 0:
        print("No hay datos de financiamiento para EX.")
        return
    if len(HL_data) == 0:
        print("No hay datos de financiamiento para Hyperliquid.")
        return
    
    # Extraer datos
    token = HL_data[0]['coin'] if HL_data else "Desconocido"

    # HL data
    times = [datetime.fromtimestamp(entry['time']/1000) for entry in HL_data]
    funding1h = [entry['funding1h'] for entry in HL_data]
    avg_funding1h = np.mean(funding1h)
    #funding8h = [entry['funding8h'] for entry in data]

    # EX data
    times_ex = [datetime.fromtimestamp(entry['time']/1000) for entry in EX_data]
    funding1h_ex = [entry['funding1h'] for entry in EX_data]
    avg_funding1h_ex = np.mean(funding1h_ex)

    spreadAvg = avg_funding1h - avg_funding1h_ex  # Cálculo del spread promedio

    # Crear el gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(times, funding1h, label='Funding 1h HL', marker='o', markersize=2)
    plt.plot(times_ex, funding1h_ex, label='Funding 1h EX', marker='x', markersize=2)
    plt.plot([], [], ' ', label=f'Avg Funding 1h HL: {avg_funding1h:.6f} = {avg_funding1h * 24* 365:.2f} APR')  # Mostrar el promedio en la leyenda
    plt.plot([], [], ' ', label=f'Avg Funding 1h EX: {avg_funding1h_ex:.6f} = {avg_funding1h_ex * 24* 365:.2f} APR')  # Mostrar el promedio en la leyenda
    plt.plot([], [], ' ', label=f'Avg Spread: {spreadAvg * 24 * 365:.2f} APR')  # Espacio para la leyenda
    # plt.plot(times, funding8h, label='Funding 8h', marker='x')

    # Estética
    plt.xlabel('Hora')
    plt.ylabel('Funding Rate (%)')
    plt.title('Funding Rates para ' + token)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("funding_comparison_chart_" + token + ".png")
    print(f"Gráfico guardado como funding_comparison_chart_{token}.png")