import numpy as np
from impl.utils.mathutil import mathutil

# 

class Asset:
    def __init__(self, symbol, prices):
        self.__symbol = symbol
        self.__prices = prices
        
        # 
        
        self.__yields = self.__calc_yields()
        
        # 
        
        return
    
    #
    
    def symbol(self):
        return self.__symbol
    
    def prices(self):
        return self.__prices
    
    #
    
    def __calc_yields(self):
        yields = []
        
        prices = self.prices()
        prices_len = len(prices)
        
        for i in range(1, prices_len):
            open_price = prices[i-1]
            close_price = prices[i]
            
            _yield = (close_price - open_price) / open_price
            
            yields.append(_yield)
        
        return np.array(yields)
    
    def yields(self):
        return self.__yields
        
    
    