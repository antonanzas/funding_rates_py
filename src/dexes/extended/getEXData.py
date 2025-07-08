import requests;
import time;

base_extended_url =  "https://api.extended.exchange/"

def get_ex_funding_history_by_token(token, startTime) -> list:
    token = token.upper() + "-USD"
    endTime = int(time.time() * 1000)
    url = f"{base_extended_url}/api/v1/info/{token}/funding?startTime={startTime}&endTime={endTime}"

    response = requests.get(url)
    transformedFunding = []

    if response.status_code == 200:
        for item in response.json()["data"]:
            coin = token.upper().replace("-USD", "")
            funding1h = float(item['f']) * 100  # Lo convierto a porcentaje
            funding8h = funding1h * 8

            transformedFunding.append({
                'coin': coin,
                'funding1h': funding1h,
                'funding8h': funding8h,
                'lapseHours': 1.0,  # Extended tiene un lapso de 1 hora entre financiamientos
                'time': item['T']
            })

        transformedFunding.reverse()

        return transformedFunding
    else:
        return []

# print(get_ex_funding_history_by_token("AAVE", int((time.time() - 7 * 86400) * 1000)))  # ultimas 7d