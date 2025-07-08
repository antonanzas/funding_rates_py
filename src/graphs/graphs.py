import matplotlib.pyplot as plt
from datetime import datetime
import time;
import numpy as np
from src.dexes.hyperliquid.getHLData import get_hyperliquid_funding_history_by_token
from src.dexes.extended.getEXData import get_ex_funding_history_by_token
from src.dexes.paradex.getPDXData import get_pdx_funding_history_by_token

hl_data = get_hyperliquid_funding_history_by_token("IP", int((time.time() - 7 * 86400) * 1000))  # Últimos 7 días
ex_data = get_ex_funding_history_by_token("IP", int((time.time() -7 * 86400) * 1000))  # Últimos 7 días
# pdx_data = get_pdx_funding_history_by_token("KAITO", int((time.time() - 15 * 86400) * 1000))  # Últimos 7 días

def plot_funding_rates(data):
    """
    Plotea las tasas de financiamiento para un token específico.

    Args:
        data (list): Lista de diccionarios con los datos de financiamiento.
    """
    # Extraer datos
    print("Datos de financiamiento:", data)
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
    plt.savefig("funding_chart_" + token + ".png")  # Guardar el gráfico como imagen

def plot_funding_rates_comparison(HL_data, EX_data):
    """
    Plotea las tasas de financiamiento para un token específico.

    Args:
        data (list): Lista de diccionarios con los datos de financiamiento.
    """

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
    plt.savefig("funding_chart_" + token + ".png")
    print(f"Gráfico guardado como funding_chart_{token}.png")

# plot_funding_rates(hl_data)  # Últimos 7 días
# plot_funding_rates(pdx_data)
plot_funding_rates_comparison(hl_data, ex_data)