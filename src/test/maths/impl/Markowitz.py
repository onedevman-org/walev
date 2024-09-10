import numpy as np

from .Asset import Asset
from .utils.mathutil import mathutil
from .Wallet import Wallet

# 

class Markowitz:
    Asset = Asset
    Wallet = Wallet
    
    # 
    
    def __init__(self, wallet):
        self.__wallet: Wallet = wallet
        
        return

    # 
    
    def wallet(self):
        return self.__wallet
    
    # 
    
    def wallet_volatility(self, expectancy):
        assets = self.wallet().assets()
        
        assets_yields = [assets[1 -1].yields(), assets[2 -1].yields()]
        yields_max_count = min(len(assets_yields[1 -1]), len(assets_yields[2 -1]))
        assets_yields[1 -1] = assets_yields[1 -1][len(assets_yields[1 -1])-yields_max_count:]
        assets_yields[2 -1] = assets_yields[2 -1][len(assets_yields[2 -1])-yields_max_count:]

        assets_expectancies = [
            mathutil.probabilities.expectancy(assets_yields[1 -1]),
            mathutil.probabilities.expectancy(assets_yields[2 -1])
        ]
        
        squared_assets_expectancies = [np.square(assets_expectancies[0]), np.square(assets_expectancies[1])]
        
        assets_expectancies_algebric_delta = assets_expectancies[1 -1] - assets_expectancies[2 -1]
        squared_assets_expectancies_algebric_delta = np.square(assets_expectancies_algebric_delta)
        
        assets_volatilities = [
            np.square(mathutil.probabilities.stddev(assets_yields[1 -1])),
            np.square(mathutil.probabilities.stddev(assets_yields[2 -1]))
        ]
        
        assets_cov = mathutil.probabilities.cov(assets_yields[1 -1], assets_yields[2 -1])
        squared_assets_cov = np.square(assets_cov)
        
        # 
        
        a = ( assets_volatilities[1 -1] + assets_volatilities[2 -1] - 2 * assets_cov ) / squared_assets_expectancies_algebric_delta
        
        b = (
            (
                (
                    4 * assets_expectancies[2 -1] * assets_cov
                    - 2 * assets_expectancies[2 -1] * assets_volatilities[1 -1]
                    - 2 * assets_expectancies[1 -1] * assets_volatilities[2 -1]
                ) / squared_assets_expectancies_algebric_delta
            )
            + (
                ( 2 * assets_cov ) / assets_expectancies_algebric_delta
            ) 
        )
        
        c = (
            (
                (
                    squared_assets_expectancies[2 -1] * assets_volatilities[1 -1]
                    + squared_assets_expectancies[1 -1] * assets_volatilities[2 -1]
                    - 2 * squared_assets_expectancies[2 -1] * np.square(assets_cov)
                ) / squared_assets_expectancies_algebric_delta
            )
            - (
                ( 2 * assets_expectancies[2 -1] * assets_cov ) / assets_expectancies_algebric_delta
            )
        )
        
        # 
        
        return ( a * np.square(expectancy) ) + ( b * expectancy ) + c

    #

    def wallet_expectancy(self, volatility):
        assets = self.wallet().assets()

        assets_yields = [assets[1 -1].yields(), assets[2 -1].yields()]
        yields_max_count = min(len(assets_yields[1 -1]), len(assets_yields[2 -1]))
        assets_yields[1 -1] = assets_yields[1 -1][len(assets_yields[1 -1])-yields_max_count:]
        assets_yields[2 -1] = assets_yields[2 -1][len(assets_yields[2 -1])-yields_max_count:]

        assets_expectancies = [
            mathutil.probabilities.expectancy(assets_yields[1 -1]),
            mathutil.probabilities.expectancy(assets_yields[2 -1])
        ]

        squared_assets_expectancies = [np.square(assets_expectancies[0]), np.square(assets_expectancies[1])]

        assets_expectancies_algebric_delta = assets_expectancies[1 -1] - assets_expectancies[2 -1]
        squared_assets_expectancies_algebric_delta = np.square(assets_expectancies_algebric_delta)

        assets_volatilities = [
            np.square(mathutil.probabilities.stddev(assets_yields[1 -1])),
            np.square(mathutil.probabilities.stddev(assets_yields[2 -1]))
        ]

        assets_cov = mathutil.probabilities.cov(assets_yields[1 -1], assets_yields[2 -1])
        squared_assets_cov = np.square(assets_cov)

        #

        # a = ( assets_volatilities[1 -1] + assets_volatilities[2 -1] - 2 * assets_cov ) / squared_assets_expectancies_algebric_delta
        #
        # b = (
        #     (
        #         (
        #             4 * assets_expectancies[2 -1] * assets_cov
        #             - 2 * assets_expectancies[2 -1] * assets_volatilities[1 -1]
        #             - 2 * assets_expectancies[1 -1] * assets_volatilities[2 -1]
        #         ) / squared_assets_expectancies_algebric_delta
        #     )
        #     + (
        #         ( 2 * assets_cov ) / assets_expectancies_algebric_delta
        #     )
        # )
        #
        # c = (
        #     (
        #         (
        #             squared_assets_expectancies[2 -1] * assets_volatilities[1 -1]
        #             + squared_assets_expectancies[1 -1] * assets_volatilities[2 -1]
        #             - 2 * squared_assets_expectancies[2 -1] * np.square(assets_cov)
        #         ) / squared_assets_expectancies_algebric_delta
        #     )
        #     - (
        #         ( 2 * assets_expectancies[2 -1] * assets_cov ) / assets_expectancies_algebric_delta
        #     )
        # )
        #
        # #
        #
        # x0 = b/(2*a)
        #
        # z1 = (1/a)
        # z2 = (-c/a) + x0*x0
        # z3 = -x0

        assets_global_volatility = ( assets_volatilities[1 -1] + assets_volatilities[2 -1] - 2 * assets_cov )
        x0 = (
            (
                (
                    2 * assets_expectancies[2 -1] * assets_cov
                    - assets_expectancies[2 -1] * assets_volatilities[1 -1]
                    - assets_expectancies[1 -1] * assets_volatilities[2 -1]
                ) / assets_global_volatility
            )
            + (
                assets_cov * assets_expectancies_algebric_delta / assets_global_volatility
            )
        )

        z1 = squared_assets_expectancies_algebric_delta / assets_global_volatility
        z2 = (
            (
                (
                    - squared_assets_expectancies[2 -1] * assets_volatilities[1 -1]
                    - squared_assets_expectancies[1 -1] * assets_volatilities[2 -1]
                    + 2 * squared_assets_expectancies[2 -1] * np.square(assets_cov)
                ) / assets_global_volatility
            )
            + (
                ( 2 * assets_expectancies[2 -1] * assets_cov ) * assets_expectancies_algebric_delta / assets_global_volatility
            )
        ) + x0*x0
        z3 = -x0

        #

        return np.sqrt((z1 * volatility) + z2) + z3

    #

    def leverage(self, risk):
        wallet_expectancy = self.wallet_expectancy(risk)

        #

        assets = self.wallet().assets()

        assets_yields = [assets[1 -1].yields(), assets[2 -1].yields()]
        yields_max_count = min(len(assets_yields[1 -1]), len(assets_yields[2 -1]))
        assets_yields[1 -1] = assets_yields[1 -1][len(assets_yields[1 -1])-yields_max_count:]
        assets_yields[2 -1] = assets_yields[2 -1][len(assets_yields[2 -1])-yields_max_count:]

        assets_expectancies = [
            mathutil.probabilities.expectancy(assets_yields[1 -1]),
            mathutil.probabilities.expectancy(assets_yields[2 -1])
        ]

        #

        print(wallet_expectancy)
        print(assets_expectancies[1 -1])
        print(assets_expectancies[2 -1])
        print(wallet_expectancy - assets_expectancies[2 -1])
        print(assets_expectancies[1 -1] - assets_expectancies[2 -1])

        return (wallet_expectancy - assets_expectancies[2 -1]) / (assets_expectancies[1 -1] - assets_expectancies[2 -1])

    #

# 