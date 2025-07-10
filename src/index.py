from src.dexes.hyperliquid.getHLData import get_all_hyperliquid_tokens, get_hyperliquid_funding_history_by_token
from src.dexes.extended.getEXData import get_ex_funding_history_by_token
from src.graphs.graphs import plot_funding_rates, plot_funding_rates_comparison
from concurrent.futures import ThreadPoolExecutor, as_completed
import time;
import numpy as np
from tabulate import tabulate

def process_token(token, timelapse):
    fundingEx = get_ex_funding_history_by_token(token, timelapse)
    if len(fundingEx) == 0:
        print(f"Insufficient data for {token} in EX.")
        return None

    fundingHL = get_hyperliquid_funding_history_by_token(token, timelapse)
    if len(fundingHL) == 0:
        print(f"Insufficient data for {token} in Hyperliquid.")
        return None

    try:
        # Avg 15 días
        fundingHL_avg_15 = np.mean([entry['funding1h'] for entry in fundingHL])
        fundingEx_avg_15 = np.mean([entry['funding1h'] for entry in fundingEx])
        spread_15 = fundingHL_avg_15 - fundingEx_avg_15

        # Avg 7 días
        fundingHL_avg_7 = np.mean([entry['funding1h'] for entry in fundingHL[-7*24:]])
        fundingEx_avg_7 = np.mean([entry['funding1h'] for entry in fundingEx[-7*24:]])
        spread_7 = fundingHL_avg_7 - fundingEx_avg_7

        # Avg 1 día
        fundingHL_avg_1 = np.mean([entry['funding1h'] for entry in fundingHL[-24:]])
        fundingEx_avg_1 = np.mean([entry['funding1h'] for entry in fundingEx[-24:]])
        spread_1 = fundingHL_avg_1 - fundingEx_avg_1

        token_profile = {
            'token': token,
            'fundingHL_avg_15d': fundingHL_avg_15,
            'fundingEx_avg_15d': fundingEx_avg_15,
            'spread_15d': abs(spread_15),
            'fundingHL_avg_7d': fundingHL_avg_7,
            'fundingEx_avg_7d': fundingEx_avg_7,
            'spread_7d': abs(spread_7),
            'fundingHL_avg_1d': fundingHL_avg_1,
            'fundingEx_avg_1d': fundingEx_avg_1,
            'spread_1d': abs(spread_1)
        }

        print(f"Token: {token}, Spread 15d: {spread_15:.6f}, Spread 7d: {spread_7:.6f}, Spread 1d: {spread_1:.6f}")
        return token_profile

    except Exception as e:
        print(f"Error processing {token}: {e}")
        return None

def search_arb_opportunities():
    """
    Busca oportunidades de arbitraje entre diferentes exchanges.
    """
    print("Starting search for arbitrage opportunities... (it should take about 1 minute)")
    tokensHL = get_all_hyperliquid_tokens()
    timelapse = int((time.time() - 15 * 86400) * 1000)

    token_profiles = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_token, token,timelapse) for token in tokensHL]

    for future in as_completed(futures):
        result = future.result()
        if result:
            token_profiles.append(result)
        

    return token_profiles

def print_top_5(opportunities, timeframe='1d'):
    """
    Imprime las 5 mejores oportunidades de arbitraje.
    """
    print(f"Top 5 Arbitrage Opportunities ({timeframe}):")
    for opp in opportunities[:5]:
        print(f"Token: {opp['token']}, Spread {timeframe}: {opp[f'spread_{timeframe}']:.6f} = {opp[f'spread_{timeframe}'] * 24 * 365:.2f} APR, "
              f"HL Avg {timeframe}: {opp[f'fundingHL_avg_{timeframe}']:.6f}, EX Avg {timeframe}: {opp[f'fundingEx_avg_{timeframe}']:.6f}")

def print_top_5_table(opportunities, timeframe='1d'):
    """
    Imprime las 5 mejores oportunidades de arbitraje como tabla.
    """
    print(f"\nTop 5 Arbitrage Opportunities ({timeframe}):")

    headers = ["Token", f"Spread {timeframe}", "APR (%)", f"HL Avg {timeframe}", f"EX Avg {timeframe}"]
    table = []

    for opp in opportunities[:5]:
        spread = opp[f'spread_{timeframe}']
        apr = spread * 24 * 365
        hl = opp[f'fundingHL_avg_{timeframe}']
        ex = opp[f'fundingEx_avg_{timeframe}']

        table.append([
            opp['token'],
            f"{spread:.6f}",
            f"{apr:.2f}",
            f"{hl:.6f}",
            f"{ex:.6f}"
        ])

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎯  Welcome to the *Arbitrage Opportunity Finder*  🎯")
    print("="*50)
    print("Please choose an option:\n")
    print("  1️⃣  Search for arbitrage opportunities")
    print("  2️⃣  Plot funding rates for a specific token")
    print("  3️⃣  Compare funding rates for a specific token")
    print("  0️⃣  Exit\n")

    choice = input("Enter your choice (0-3): ").strip()

    if choice == '0':
        print("Exiting the program. Goodbye! 👋")
        exit()
    elif choice == '1':
        opportunities = search_arb_opportunities()
        print("Arbitrage Opportunities:")
        opportunities.sort(key=lambda x: x['spread_1d'], reverse=True)
        print_top_5_table(opportunities)
        opportunities.sort(key=lambda x: x['spread_7d'], reverse=True)
        print_top_5_table(opportunities,'7d')
        opportunities.sort(key=lambda x: x['spread_15d'], reverse=True)
        print_top_5_table(opportunities,'15d')
    elif choice == '2':
        token = input("Enter the token symbol (e.g., ETH, BTC): ").strip().upper()
        timelapse = input("Enter the time period in days (default is 1, max 31): ").strip() or '1'
        platform = input("Enter the platform (HL, EX, default is HL): ").strip().upper() or 'HL'
        plot_funding_rates(token, int(timelapse), platform)
    elif choice == '3':
        token = input("Enter the token symbol (e.g., ETH, BTC): ").strip().upper()
        timelapse = input("Enter the time period in days (default is 7, max 31): ").strip() or '7'
        print(f"Comparing funding rates of hyperliquid and extended")
        plot_funding_rates_comparison(token, int(timelapse))


        
            
            
        