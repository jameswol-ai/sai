import requests


class ExchangeConnector:


    def __init__(self):

        self.mode="demo"



    def get_price(self, symbol="BTCUSDT"):


        if self.mode=="demo":

            return {
                "symbol":symbol,
                "price":65000,
                "volume":1200
            }


        url = (
            "https://api.binance.com"
            "/api/v3/ticker/24hr"
        )


        response=requests.get(
            url,
            params={
                "symbol":symbol
            },
            timeout=10
        )


        data=response.json()


        return {

            "symbol":symbol,

            "price":
                float(
                    data["lastPrice"]
                ),

            "volume":
                float(
                    data["volume"]
                )

        }