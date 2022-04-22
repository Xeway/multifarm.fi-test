import requests as req

def getPrices(tokens):
    for token in tokens:
        res = req.get('https://api.coingecko.com/api/v3/simple/price?ids=' + token + '&vs_currencies=usd')
        if (res.status_code == 200):
            tokens[token] = res.json()[token]['usd']