import random


class MarketEngine:


    def get_market(self):

        price = round(
            random.uniform(
                50000,
                70000
            ),
            2
        )


        return {

            "symbol":"BTC/USDT",

            "price":price,

            "volume":
                random.randint(
                    1000,
                    5000
                )

        }