import subprocess

outputfiat = subprocess.check_output(['java', '-jar', 'fiat.jar'])
datafiat = [line.decode('utf-8').strip() for line in outputfiat.splitlines()]

CurUSDValue, diffUSD, PercentUSD, CurEURValue, diffEUR, PercentEUR, CurCNYValue, diffCNY, PercentCNY = [round(float(value), 2) if "." in value else int(value) for value in datafiat]
CurUSDValue = str(CurUSDValue) + "₽"
CurEURValue = str(CurEURValue) + "₽"
CurCNYValue = str(CurCNYValue) + "₽"

diffUSD = "🔺 " + str(abs(diffUSD)) + "₽" if diffUSD < 0 else "🔻 " + str(diffUSD) + "₽"
diffEUR = "🔺 " + str(abs(diffEUR)) + "₽" if diffEUR < 0 else "🔻 " + str(diffEUR) + "₽"
diffCNY = "🔺 " + str(abs(diffCNY)) + "₽" if diffCNY < 0 else "🔻 " + str(diffCNY) + "₽"

PercentUSD = str(PercentUSD) + "%"
PercentEUR = str(PercentEUR) + "%"
PercentCNY = str(PercentCNY) + "%"

outputUSDdigest = f"💵 1 $ = {CurUSDValue} {diffUSD} ({PercentUSD})"
outputEURdigest = f"💶 1 € = {CurEURValue} {diffEUR} ({PercentEUR})"
outputCNYdigest = f"💴 1 ¥ = {CurCNYValue} {diffCNY} ({PercentCNY})"
print('pustoFiat (re)loaded')