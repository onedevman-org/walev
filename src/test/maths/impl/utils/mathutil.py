import numpy as np
import pandas as pd
import scipy as sp

# 

class mathutil:
    
    class probabilities:
        
        def expectancy(values, p=[]):
            l_p = len(p)
            isNPArray = isinstance(values, np.ndarray)

            if isNPArray:
                return (values * p).sum() if l_p > 0 else (values.sum() / len(values))
            else:
                l_values = len(values)
                result = 0

                if l_p > 0:
                    for i in range(l_values):
                        result += values[i] * p[i]
                else:
                    for i in range(l_values):
                        result += values[i]
                    result = result / l_values

                return result
        
        # 
        
        def stddev(values):
            expectancy = mathutil.probabilities.expectancy(values)
            delta = np.abs(values - expectancy) if isinstance(values, np.ndarray) else np.array([value - expectancy for value in values])
            return np.sqrt((delta * delta).sum() / len(values))
        
        # 
        
        def correlation(xvalues, yvalues):
            x_count = len(xvalues)
            y_count = len(yvalues)

            if x_count != y_count:
                raise RuntimeError("x and y set value count should be the same.")
            
            x_expectancy = mathutil.probabilities.expectancy(xvalues)
            y_expectancy = mathutil.probabilities.expectancy(yvalues)

            x_deviation = (xvalues - x_expectancy) if isinstance(xvalues, np.ndarray) else np.array([value - x_expectancy for value in xvalues])
            y_deviation = (yvalues - y_expectancy) if isinstance(yvalues, np.ndarray) else np.array([value - y_expectancy for value in yvalues])

            return (x_deviation * y_deviation).sum() / np.sqrt((x_deviation * x_deviation).sum() * (y_deviation * y_deviation).sum())
        
        # 
        
        def cov(xvalues, yvalues):
            return mathutil.probabilities.correlation(xvalues, yvalues) * mathutil.probabilities.stddev(xvalues) * mathutil.probabilities.stddev(yvalues)
        
        # 
        
        class normallaw:
            def density_by_stddev(m, d, x):
                return (1 / (d * np.sqrt(2 * np.pi))) * np.exp(- ((x - m) * (x - m)) / (2 * d * d))
            
#