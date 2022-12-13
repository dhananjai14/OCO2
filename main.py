from CO2.exception import CO2_Exception
import sys
try:
    a ,b = 10 , 0
    print(a/b)
except Exception as e:
    raise CO2_Exception(sys)
