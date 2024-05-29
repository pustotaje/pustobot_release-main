import subprocess
from decimal import Decimal

outputcrypto = subprocess.check_output(['java', '-jar', 'crypto.jar'])
datacrypto = [line.decode('utf-8').strip() for line in outputcrypto.splitlines()]

crypto_data = {}

current_currency = None

def normalize_number(value):
    try:
        if "BTC" in current_currency:
            return round(Decimal(value),1)
        elif "TONCOIN" in current_currency:
            return round(Decimal(value),3)
        elif "MATIC" in current_currency:
            return round(Decimal(value),3)
        elif "BNB" in current_currency:
            return round(Decimal(value),3)
        elif "XRP" in current_currency:
            return round(Decimal(value),4)
        elif "ETH" in current_currency:
            return round(Decimal(value),1)
        elif "SHIB" in current_currency:
            return round(Decimal(value), 6)
        elif "DOGE" in current_currency:
            return round(Decimal(value), 4)
        elif "LTC" in current_currency:
            return round(Decimal(value), 3)
        elif "TRX" in current_currency:
            return round(Decimal(value), 4)
        else:
            return value
    except:
        return value

for line in datacrypto:
    if line.startswith("Currency:"):
        if current_currency is not None:
            crypto_data[current_currency] = currency_dict
        current_currency = line.split("Currency: ")[1].strip()
        currency_dict = {}
    else:
        key_value = line.split(": ")
        if len(key_value) == 2:
            key, value = key_value
            currency_dict[key.strip()] = normalize_number(value.strip())

if current_currency is not None:
    crypto_data[current_currency] = currency_dict

def generate_output(currency, data):
    price = data.get("Price", "")
    change_day = Decimal(data.get("Change Day", 0))
    change_pct_day = Decimal(data.get("Change Pct Day", 0))

    change_day_symbol = "🤏​" if change_day == Decimal("0.00") else ("🔻" if change_day < Decimal("0.00") else "🔺")
    change_pct_day_symbol = "🤏​" if change_pct_day == Decimal("0.00") else "🔻" if change_pct_day < Decimal("0.00") else "🔺"

    output = f"1 {currency} = {price}$; {change_day_symbol} {abs(change_day)}$ \n({change_pct_day_symbol} {abs(change_pct_day)}%)"
    return output

def genout(currency):
    return generate_output(currency, crypto_data[currency])

print('pustoCrypto (re)loaded')